module Helpers exposing
    ( archiveCell
    , calculateSmsCost
    , decodeAlwaysTrue
    , formatDate
    , handleNotSaved
    , onClick
    , toggleSelectedPk
    )

import Css
import Date
import DateFormat
import Html exposing (Attribute, Html, a, text)
import Html.Attributes exposing (id)
import Html.Events exposing (onWithOptions)
import Json.Decode as Decode
import List.Extra as LE
import Notification as Notif


toggleSelectedPk : Int -> List Int -> List Int
toggleSelectedPk pk pks =
    case List.member pk pks of
        True ->
            LE.remove pk pks

        False ->
            pk :: pks


decodeAlwaysTrue : Decode.Decoder Bool
decodeAlwaysTrue =
    Decode.succeed True



-- update model after http errors:


handleNotSaved : { a | notifications : Notif.Notifications } -> ( { a | notifications : Notif.Notifications }, List (Cmd msg) )
handleNotSaved model =
    ( { model | notifications = Notif.addNotSaved model.notifications }, [] )



-- Pretty date format


formatDate : Maybe Date.Date -> String
formatDate date =
    case date of
        Just d ->
            DateFormat.format
                [ DateFormat.hourMilitaryFixed
                , DateFormat.text ":"
                , DateFormat.minuteFixed
                , DateFormat.text " - "
                , DateFormat.dayOfMonthSuffix
                , DateFormat.text " "
                , DateFormat.monthNameFirstThree
                ]
                d

        Nothing ->
            ""



-- calculate cost of sending an sms


calculateSmsCost : Float -> String -> Float
calculateSmsCost smsCostPerMsg msg =
    msg
        |> String.length
        |> toFloat
        |> flip (/) 160
        |> ceiling
        |> toFloat
        |> (*) smsCostPerMsg


archiveCell : Bool -> msg -> Html msg
archiveCell isArchived msg =
    a
        [ Css.btn
        , Css.btn_grey
        , Css.text_sm
        , onClick msg
        , id "archiveItemButton"
        ]
        [ text <| archiveText isArchived ]


archiveText : Bool -> String
archiveText isArchived =
    case isArchived of
        True ->
            "UnArchive"

        False ->
            "Archive"


onClick : msg -> Attribute msg
onClick message =
    onWithOptions "click" { stopPropagation = True, preventDefault = True } (Decode.succeed message)
