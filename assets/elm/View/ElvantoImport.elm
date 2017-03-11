module View.ElvantoImport exposing (view)

import Helpers exposing (formatDate)
import Html exposing (..)
import Html.Attributes exposing (class, id)
import Html.Events exposing (onClick)
import Messages exposing (..)
import Models.Apostello exposing (ElvantoGroup)
import Regex
import View.FilteringTable exposing (filteringTable)


-- Main view


view : Regex.Regex -> List ElvantoGroup -> Html Msg
view filterRegex groups =
    div []
        [ div [ class "ui fluid buttons" ]
            [ fetchButton
            , pullButton
            ]
        , br [] []
        , filteringTable "ui striped compact definition table" tableHead filterRegex groupRow groups
        ]


tableHead : Html Msg
tableHead =
    thead []
        [ tr []
            [ th [] []
            , th [] [ text "Last Synced" ]
            , th [] [ text "Sync?" ]
            ]
        ]


fetchButton : Html Msg
fetchButton =
    a [ class "ui green button", onClick (ElvantoMsg FetchGroups), id "fetch_button" ] [ text "Fetch Groups" ]


pullButton : Html Msg
pullButton =
    a [ class "ui blue button", onClick (ElvantoMsg PullGroups), id "pull_button" ] [ text "Pull Groups" ]


groupRow : ElvantoGroup -> Html Msg
groupRow group =
    tr []
        [ td [] [ text group.name ]
        , td [] [ text (formatDate group.last_synced) ]
        , td [] [ toggleSyncButton group ]
        ]


toggleSyncButton : ElvantoGroup -> Html Msg
toggleSyncButton group =
    case group.sync of
        True ->
            syncingButton group

        False ->
            notSyncingButton group


syncingButton : ElvantoGroup -> Html Msg
syncingButton group =
    button_ "ui tiny green button" "Syncing" group


notSyncingButton : ElvantoGroup -> Html Msg
notSyncingButton group =
    button_ "ui tiny grey button" "Disabled" group


button_ : String -> String -> ElvantoGroup -> Html Msg
button_ styling label group =
    a [ class styling, onClick (ElvantoMsg (ToggleGroupSync group)) ] [ text label ]
