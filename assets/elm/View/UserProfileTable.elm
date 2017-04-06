module View.UserProfileTable exposing (view)

import Formatting as F exposing ((<>))
import Html exposing (Html, thead, tr, th, text, a, i, button, td)
import Html.Attributes exposing (class, href)
import Html.Events exposing (onClick)
import Messages exposing (Msg(UserProfileTableMsg), UserProfileTableMsg(ToggleField))
import Models.Apostello exposing (UserProfile)
import Regex
import View.FilteringTable exposing (filteringTable)


-- Main view


view : Regex.Regex -> List UserProfile -> Html Msg
view filterRegex profiles =
    filteringTable "ui collapsing celled very basic table" tableHead filterRegex userprofileRow profiles


tableHead : Html Msg
tableHead =
    thead []
        [ tr [ class "left aligned" ]
            [ th [] [ text "User" ]
            , th [] [ text "Approved" ]
            , th [] [ text "Keywords" ]
            , th [] [ text "Send SMS" ]
            , th [] [ text "Contacts" ]
            , th [] [ text "Groups" ]
            , th [] [ text "Incoming" ]
            , th [] [ text "Outgoing" ]
            , th [] [ text "Archiving" ]
            ]
        ]


userprofileRow : UserProfile -> Html Msg
userprofileRow userprofile =
    tr [ class "center aligned" ]
        [ td []
            [ a
                [ href (F.print (F.s "/users/profiles/" <> F.int <> F.s "/") userprofile.pk)
                ]
                [ text userprofile.user.email ]
            ]
        , toggleCell userprofile Approved
        , toggleCell userprofile Keywords
        , toggleCell userprofile SendSMS
        , toggleCell userprofile Contacts
        , toggleCell userprofile Groups
        , toggleCell userprofile Incoming
        , toggleCell userprofile Outgoing
        , toggleCell userprofile Archiving
        ]


toggleCell : UserProfile -> Field -> Html Msg
toggleCell userprofile field =
    let
        fieldVal =
            lookupField field userprofile

        buttonType =
            case fieldVal of
                True ->
                    "positive"

                False ->
                    "negative"

        className =
            "ui tiny " ++ buttonType ++ " icon button"

        iconType =
            case fieldVal of
                True ->
                    "checkmark icon"

                False ->
                    "minus circle icon"
    in
        td []
            [ button [ class className, onClick (UserProfileTableMsg (ToggleField (toggleField field userprofile))) ]
                [ i [ class iconType ] []
                ]
            ]


lookupField : Field -> UserProfile -> Bool
lookupField fieldName profile =
    case fieldName of
        Approved ->
            profile.approved

        Keywords ->
            profile.can_see_keywords

        SendSMS ->
            profile.can_send_sms

        Contacts ->
            profile.can_see_contact_names

        Groups ->
            profile.can_see_groups

        Incoming ->
            profile.can_see_incoming

        Outgoing ->
            profile.can_see_outgoing

        Archiving ->
            profile.can_archive


toggleField : Field -> UserProfile -> UserProfile
toggleField field profile =
    case field of
        Approved ->
            { profile | approved = not profile.approved }

        Keywords ->
            { profile | can_see_keywords = not profile.can_see_keywords }

        SendSMS ->
            { profile | can_send_sms = not profile.can_send_sms }

        Contacts ->
            { profile | can_see_contact_names = not profile.can_see_contact_names }

        Groups ->
            { profile | can_see_groups = not profile.can_see_groups }

        Incoming ->
            { profile | can_see_incoming = not profile.can_see_incoming }

        Outgoing ->
            { profile | can_see_outgoing = not profile.can_see_outgoing }

        Archiving ->
            { profile | can_archive = not profile.can_archive }


type Field
    = Approved
    | Keywords
    | SendSMS
    | Contacts
    | Groups
    | Incoming
    | Outgoing
    | Archiving
