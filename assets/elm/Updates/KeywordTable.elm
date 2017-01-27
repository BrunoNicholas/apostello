module Updates.KeywordTable exposing (update)

import Actions exposing (determineRespCmd)
import Decoders exposing (keywordDecoder)
import DjangoSend exposing (post)
import Helpers exposing (..)
import Http
import Json.Encode as Encode
import Messages exposing (..)
import Models exposing (..)


update : KeywordTableMsg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        LoadKeywordTableResp (Ok resp) ->
            ( { model
                | loadingStatus = determineLoadingStatus resp
                , keywordTable = updateKeywords model.keywordTable resp
              }
            , determineRespCmd KeywordTable resp
            )

        LoadKeywordTableResp (Err _) ->
            handleLoadingFailed model

        ToggleKeywordArchive isArchived pk ->
            ( { model
                | keywordTable = optArchiveKeyword model.keywordTable pk
              }
            , toggleKeywordArchive model.csrftoken isArchived pk
            )

        ReceiveToggleKeywordArchive (Ok _) ->
            ( model, Cmd.none )

        ReceiveToggleKeywordArchive (Err _) ->
            handleNotSaved model


optArchiveKeyword : KeywordTableModel -> Int -> KeywordTableModel
optArchiveKeyword model pk =
    { model | keywords = List.filter (\r -> not (r.pk == pk)) model.keywords }


updateKeywords : KeywordTableModel -> ApostelloResponse Keyword -> KeywordTableModel
updateKeywords model resp =
    { model | keywords = mergeItems model.keywords resp.results |> List.sortBy .keyword }


toggleKeywordArchive : CSRFToken -> Bool -> Int -> Cmd Msg
toggleKeywordArchive csrftoken isArchived pk =
    let
        url =
            "/api/v1/keywords/" ++ (toString pk)

        body =
            encodeBody [ ( "archived", Encode.bool isArchived ) ]
    in
        post url body csrftoken keywordDecoder
            |> Http.send (KeywordTableMsg << ReceiveToggleKeywordArchive)
