module Views.OutboundTable exposing (view)

import Helpers exposing (formatDate)
import Html exposing (..)
import Html.Attributes exposing (class, href, style)
import Messages exposing (..)
import Models exposing (..)
import Regex
import Views.FilteringTable exposing (uiTable)


-- Main view


view : Regex.Regex -> OutboundTableModel -> Html Messages.Msg
view filterRegex model =
    let
        head =
            thead []
                [ tr []
                    [ th [] [ text "To" ]
                    , th [] [ text "Message" ]
                    , th [] [ text "Sent" ]
                    ]
                ]
    in
        uiTable head filterRegex smsRow model.sms


smsRow : SmsOutbound -> Html Messages.Msg
smsRow sms =
    let
        recipient =
            case sms.recipient of
                Just r ->
                    r

                Nothing ->
                    { full_name = "", pk = 0 }
    in
        tr []
            [ td [ class "collapsing" ] [ a [ href ("/recipient/edit/" ++ (toString recipient.pk)), style [ ( "color", "#212121" ) ] ] [ text recipient.full_name ] ]
            , td [] [ text sms.content ]
            , td [ class "collapsing" ] [ text (formatDate sms.time_sent) ]
            ]
