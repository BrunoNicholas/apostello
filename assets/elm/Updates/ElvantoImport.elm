module Updates.ElvantoImport exposing (update)

import Actions exposing (determineRespCmd)
import Decoders exposing (elvantogroupDecoder)
import DjangoSend exposing (post)
import Helpers exposing (..)
import Http
import Json.Decode as Decode
import Json.Encode as Encode
import Messages exposing (..)
import Models exposing (..)
import Updates.Notification exposing (createInfoNotification, createSuccessNotification)


update : ElvantoMsg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        LoadElvantoResp (Ok resp) ->
            ( { model
                | loadingStatus = determineLoadingStatus resp
                , elvantoImport = updateGroups model.elvantoImport resp.results
              }
            , determineRespCmd ElvantoImport resp
            )

        LoadElvantoResp (Err _) ->
            handleLoadingFailed model

        ToggleGroupSync group ->
            ( { model | elvantoImport = optToggleGroup group model.elvantoImport }
            , toggleElvantoGroupSync model.csrftoken group
            )

        ReceiveToggleGroupSync (Ok group) ->
            ( { model
                | elvantoImport = updateGroups model.elvantoImport [ group ]
              }
            , Cmd.none
            )

        ReceiveToggleGroupSync (Err _) ->
            handleNotSaved model

        PullGroups ->
            ( createInfoNotification model "Groups are being imported, it may take a couple of minutes"
            , pullGroups model.csrftoken
            )

        FetchGroups ->
            ( createSuccessNotification model "Groups are being fetched, it may take a couple of minutes"
            , fetchGroups model.csrftoken
            )

        ReceiveButtonResp (Ok _) ->
            ( model, Cmd.none )

        ReceiveButtonResp (Err _) ->
            handleNotSaved model


updateGroups : ElvantoImportModel -> ElvantoGroups -> ElvantoImportModel
updateGroups model newGroups =
    { model
        | groups =
            mergeItems model.groups newGroups
                |> List.sortBy .name
    }


pullGroups : String -> Cmd Msg
pullGroups csrftoken =
    post "/api/v1/elvanto/group_pull/" (encodeBody []) csrftoken (Decode.succeed True)
        |> Http.send (ElvantoMsg << ReceiveButtonResp)


fetchGroups : String -> Cmd Msg
fetchGroups csrftoken =
    post "/api/v1/elvanto/group_fetch/" (encodeBody []) csrftoken (Decode.succeed True)
        |> Http.send (ElvantoMsg << ReceiveButtonResp)


toggleElvantoGroupSync : CSRFToken -> ElvantoGroup -> Cmd Msg
toggleElvantoGroupSync csrftoken group =
    let
        url =
            "/api/v1/elvanto/group/" ++ (toString group.pk)

        body =
            encodeBody [ ( "sync", Encode.bool group.sync ) ]
    in
        post url body csrftoken elvantogroupDecoder
            |> Http.send (ElvantoMsg << ReceiveToggleGroupSync)


optToggleGroup : ElvantoGroup -> ElvantoImportModel -> ElvantoImportModel
optToggleGroup group model =
    { model | groups = List.map (toggleGroupSync group.pk) model.groups }


toggleGroupSync : Int -> ElvantoGroup -> ElvantoGroup
toggleGroupSync pk group =
    if pk == group.pk then
        { group | sync = (not group.sync) }
    else
        group
