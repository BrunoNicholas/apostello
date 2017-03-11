module View.InboundTable exposing (view)

import Helpers exposing (formatDate)
import Html exposing (..)
import Html.Attributes exposing (class, href, style)
import Html.Events exposing (onClick)
import Messages exposing (..)
import Models.Apostello exposing (SmsInbound)
import Pages exposing (Page(SendAdhoc))
import Regex
import View.Helpers exposing (spaLink)
import View.FilteringTable exposing (uiTable)


-- Main view


view : Regex.Regex -> List SmsInbound -> Html Msg
view filterRegex sms =
    let
        head =
            thead []
                [ tr []
                    [ th [] [ text "From" ]
                    , th [] [ text "Keyword" ]
                    , th [] [ text "Message" ]
                    , th [] [ text "Time" ]
                    , th [] []
                    ]
                ]
    in
        uiTable head filterRegex smsRow sms


smsRow : SmsInbound -> Html Msg
smsRow sms =
    tr [ style [ ( "backgroundColor", sms.matched_colour ) ] ]
        [ recipientCell sms
        , keywordCell sms
        , td [] [ text sms.content ]
        , td [ class "collapsing" ] [ text (formatDate sms.time_received) ]
        , reprocessCell sms
        ]


recipientCell : SmsInbound -> Html Msg
recipientCell sms =
    let
        replyPage =
            SendAdhoc Nothing <| Maybe.map List.singleton sms.sender_pk

        contactLink =
            case sms.sender_url of
                Just url ->
                    url

                Nothing ->
                    "#"
    in
        td []
            [ spaLink a [] [ i [ class "violet reply link icon" ] [] ] replyPage
            , a [ href contactLink, style [ ( "color", "#212121" ) ] ] [ text sms.sender_name ]
            ]


keywordCell : SmsInbound -> Html Msg
keywordCell sms =
    case sms.matched_keyword of
        "#" ->
            td [] [ b [] [ text sms.matched_keyword ] ]

        _ ->
            td []
                [ b []
                    [ a [ href sms.matched_link, style [ ( "color", "#212121" ) ] ] [ text sms.matched_keyword ]
                    ]
                ]


reprocessCell : SmsInbound -> Html Msg
reprocessCell sms =
    td [ class "collapsing" ]
        [ a [ class "ui tiny blue button", onClick (InboundTableMsg (ReprocessSms sms.pk)) ] [ text "Reprocess" ]
        ]
