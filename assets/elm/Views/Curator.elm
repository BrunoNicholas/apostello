module Views.Curator exposing (view)

import Helpers exposing (formatDate)
import Html exposing (..)
import Html.Attributes exposing (class, href, style)
import Html.Events exposing (onClick)
import Messages exposing (..)
import Models exposing (..)
import Regex
import Views.FilteringTable exposing (uiTable)


-- Main view


view : Regex.Regex -> WallModel -> Html Msg
view filterRegex model =
    let
        head =
            thead []
                [ tr []
                    [ th [] [ text "Message" ]
                    , th [] [ text "Time" ]
                    , th [] [ text "Display?" ]
                    ]
                ]
    in
        uiTable head filterRegex smsRow model.sms


smsRow : SmsInboundSimple -> Html Msg
smsRow sms =
    tr []
        [ td [] [ text sms.content ]
        , td [ class "collapsing" ] [ text (formatDate sms.time_received) ]
        , curateToggleCell sms
        ]


curateToggleCell : SmsInboundSimple -> Html Msg
curateToggleCell sms =
    let
        text_ =
            case sms.display_on_wall of
                True ->
                    "Showing"

                False ->
                    "Hidden"

        colour =
            case sms.display_on_wall of
                True ->
                    "green"

                False ->
                    "red"

        className =
            "ui tiny " ++ colour ++ " fluid button"
    in
        td [ class "collapsing" ]
            [ a
                [ class className
                , onClick (WallMsg (ToggleWallDisplay sms.display_on_wall sms.pk))
                ]
                [ text text_ ]
            ]
