package api

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/merico-dev/lake/config"
	"github.com/merico-dev/lake/models/common"

	"github.com/go-playground/validator/v10"
	"github.com/merico-dev/lake/plugins/core"
	"github.com/merico-dev/lake/plugins/tapd/models"
	"github.com/mitchellh/mapstructure"
)

func findSourceByInputParam(input *core.ApiResourceInput) (*models.TapdSource, error) {
	sourceId := input.Params["sourceId"]
	if sourceId == "" {
		return nil, fmt.Errorf("missing sourceid")
	}
	tapdSourceId, err := strconv.ParseUint(sourceId, 10, 64)
	if err != nil {
		return nil, fmt.Errorf("invalid sourceId")
	}

	return getTapdSourceById(tapdSourceId)
}

func getTapdSourceById(id uint64) (*models.TapdSource, error) {
	tapdSource := &models.TapdSource{}
	err := db.First(tapdSource, id).Error
	if err != nil {
		return nil, err
	}

	// decrypt
	v := config.GetConfig()
	encKey := v.GetString(core.EncodeKeyEnvStr)
	tapdSource.BasicAuthEncoded, err = core.Decrypt(encKey, tapdSource.BasicAuthEncoded)
	if err != nil {
		return nil, err
	}

	return tapdSource, nil
}

func mergeFieldsToTapdSource(tapdSource *models.TapdSource, sources ...map[string]interface{}) error {
	// decode
	for _, source := range sources {
		err := mapstructure.Decode(source, tapdSource)
		if err != nil {
			return err
		}
	}

	// validate
	vld := validator.New()
	err := vld.Struct(tapdSource)
	if err != nil {
		return err
	}

	return nil
}

func refreshAndSaveTapdSource(tapdSource *models.TapdSource, data map[string]interface{}) error {
	var err error
	// update fields from request body
	err = mergeFieldsToTapdSource(tapdSource, data)
	if err != nil {
		return err
	}

	// encrypt
	v := config.GetConfig()
	encKey := v.GetString(core.EncodeKeyEnvStr)
	if encKey == "" {
		// Randomly generate a bunch of encryption keys and set them to config
		encKey = core.RandomEncKey()
		v.Set(core.EncodeKeyEnvStr, encKey)
		err := v.WriteConfig()
		if err != nil {
			return err
		}
	}
	tapdSource.BasicAuthEncoded, err = core.Encrypt(encKey, tapdSource.BasicAuthEncoded)
	if err != nil {
		return err
	}

	// transaction for nested operations
	tx := db.Begin()
	defer func() {
		if err != nil {
			tx.Rollback()
		} else {
			tx.Commit()
		}
	}()
	if tapdSource.RateLimit == 0 {
		tapdSource.RateLimit = 10800
	}
	if tapdSource.ID > 0 {
		err = tx.Save(tapdSource).Error
	} else {
		err = tx.Create(tapdSource).Error
	}
	if err != nil {
		if common.IsDuplicateError(err) {
			return fmt.Errorf("tapd source with name %s already exists", tapdSource.Name)
		}
		return err
	}
	tapdSource.BasicAuthEncoded, err = core.Decrypt(encKey, tapdSource.BasicAuthEncoded)
	if err != nil {
		return err
	}
	return nil
}

/*
POST /plugins/tapd/sources
{
	"name": "tapd data source name",
	"endpoint": "tapd api endpoint, i.e. https://merico.atlassian.net/rest",
	"basicAuthEncoded": "generated by `echo -n <tapd login email>:<tapd token> | base64`",
	"rateLimit": 10800,
}
*/
func PostSources(input *core.ApiResourceInput) (*core.ApiResourceOutput, error) {
	// create a new source
	tapdSource := &models.TapdSource{}

	// update from request and save to database
	err := refreshAndSaveTapdSource(tapdSource, input.Body)
	if err != nil {
		return nil, err
	}

	return &core.ApiResourceOutput{Body: tapdSource, Status: http.StatusCreated}, nil
}

/*
PUT /plugins/tapd/sources/:sourceId
{
	"name": "tapd data source name",
	"endpoint": "tapd api endpoint, i.e. https://merico.atlassian.net/rest",
	"basicAuthEncoded": "generated by `echo -n <tapd login email>:<tapd token> | base64`",
	"rateLimit": 10800,
}
*/
func PutSource(input *core.ApiResourceInput) (*core.ApiResourceOutput, error) {
	// load from db
	tapdSource, err := findSourceByInputParam(input)
	if err != nil {
		return nil, err
	}

	// update from request and save to database
	err = refreshAndSaveTapdSource(tapdSource, input.Body)
	if err != nil {
		return nil, err
	}

	return &core.ApiResourceOutput{Body: tapdSource}, nil
}

/*
DELETE /plugins/tapd/sources/:sourceId
*/
func DeleteSource(input *core.ApiResourceInput) (*core.ApiResourceOutput, error) {
	// load from db
	tapdSource, err := findSourceByInputParam(input)
	if err != nil {
		return nil, err
	}
	err = db.Delete(tapdSource).Error
	if err != nil {
		return nil, err
	}

	return &core.ApiResourceOutput{Body: tapdSource}, nil
}

/*
GET /plugins/tapd/sources
*/
func ListSources(input *core.ApiResourceInput) (*core.ApiResourceOutput, error) {
	tapdSources := make([]models.TapdSource, 0)
	err := db.Find(&tapdSources).Error
	if err != nil {
		return nil, err
	}
	return &core.ApiResourceOutput{Body: tapdSources}, nil
}

/*
GET /plugins/tapd/sources/:sourceId


{
	"name": "tapd data source name",
	"endpoint": "tapd api endpoint, i.e. https://merico.atlassian.net/rest",
	"basicAuthEncoded": "generated by `echo -n <tapd login email>:<tapd token> | base64`",
	"rateLimit": 10800,
}
*/
func GetSource(input *core.ApiResourceInput) (*core.ApiResourceOutput, error) {
	tapdSource, err := findSourceByInputParam(input)
	if err != nil {
		return nil, err
	}

	detail := &models.TapdSourceDetail{
		TapdSource: *tapdSource,
	}
	return &core.ApiResourceOutput{Body: detail}, nil
}

type WorkspaceResponse struct {
	Id    uint64
	Title string
	Value string
}

// GET /plugins/tapd/sources/:sourceId/boards

func GetBoardsBySourceId(input *core.ApiResourceInput) (*core.ApiResourceOutput, error) {
	sourceId := input.Params["sourceId"]
	if sourceId == "" {
		return nil, fmt.Errorf("missing sourceid")
	}
	tapdSourceId, err := strconv.ParseUint(sourceId, 10, 64)
	if err != nil {
		return nil, fmt.Errorf("invalid sourceId")
	}
	var tapdWorkspaces []models.TapdWorkspace
	err = db.Where("source_Id = ?", tapdSourceId).Find(&tapdWorkspaces).Error
	if err != nil {
		return nil, err
	}
	var workSpaceResponses []WorkspaceResponse
	for _, workSpace := range tapdWorkspaces {
		workSpaceResponses = append(workSpaceResponses, WorkspaceResponse{
			Id:    uint64(workSpace.ID),
			Title: workSpace.Name,
			Value: fmt.Sprintf("%v", workSpace.ID),
		})
	}
	return &core.ApiResourceOutput{Body: workSpaceResponses}, nil
}
