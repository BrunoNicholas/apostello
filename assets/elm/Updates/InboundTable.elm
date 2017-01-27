module Updates.InboundTable exposing (update)

import Actions exposing (determineRespCmd)
import Decoders exposing (smsinboundDecoder)
import DjangoSend exposing (post)
import Helpers exposing (..)
import Http
import Json.Encode as Encode
import Messages exposing (..)
import Models exposing (..)


update : InboundTableMsg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        LoadInboundTableResp (Ok resp) ->
            ( { model
                | loadingStatus = determineLoadingStatus resp
                , inboundTable = updateSms model.inboundTable resp.results
              }
            , determineRespCmd InboundTable resp
            )

        LoadInboundTableResp (Err _) ->
            handleLoadingFailed model

        ReprocessSms pk ->
            ( model, reprocessSms model.csrftoken pk )

        ReceiveReprocessSms (Ok sms) ->
            ( { model | inboundTable = updateSms model.inboundTable [ sms ] }, Cmd.none )

        ReceiveReprocessSms (Err _) ->
            handleNotSaved model


updateSms : InboundTableModel -> SmsInbounds -> InboundTableModel
updateSms model newSms =
    { model
        | sms =
            mergeItems model.sms newSms
                |> List.sortBy compareByTR
                |> List.reverse
    }


reprocessSms : CSRFToken -> Int -> Cmd Msg
reprocessSms csrftoken pk =
    let
        url =
            "/api/v1/sms/in/" ++ (toString pk)

        body =
            encodeBody [ ( "reingest", Encode.bool True ) ]
    in
        post url body csrftoken smsinboundDecoder
            |> Http.send (InboundTableMsg << ReceiveReprocessSms)
