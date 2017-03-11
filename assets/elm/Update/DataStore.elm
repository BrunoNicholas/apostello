module Update.DataStore exposing (..)

import Date
import Dict
import Models exposing (Model, DataStore)
import Models.Remote exposing (RemoteDataType(..), RawResponse, dataFromResp)
import Models.Apostello exposing (..)


updateNewData : RemoteDataType -> RawResponse -> Model -> Model
updateNewData dt rawResp model =
    case dt of
        OutgoingSms ->
            { model | dataStore = updateSmsOutbounds model.dataStore (dataFromResp decodeSmsOutbound rawResp) }

        IncomingSms ->
            { model | dataStore = updateSmsInbounds model.dataStore (dataFromResp decodeSmsInbound rawResp) }

        Groups ->
            { model | dataStore = updateGroups model.dataStore (dataFromResp decodeRecipientGroup rawResp) }

        Contacts ->
            { model | dataStore = updateRecipients model.dataStore (dataFromResp decodeRecipient rawResp) }

        Keywords ->
            { model | dataStore = updateKeywords model.dataStore (dataFromResp decodeKeyword rawResp) }

        ElvantoGroups ->
            { model | dataStore = updateElvantoGroups model.dataStore (dataFromResp decodeElvantoGroup rawResp) }

        UserProfiles ->
            { model | dataStore = updateUserProfiles model.dataStore (dataFromResp decodeUserProfile rawResp) }

        ScheduledSms ->
            { model | dataStore = updateQueuedSms model.dataStore (dataFromResp decodeQueuedSms rawResp) }



-- Helpers


updateSmsOutbounds : DataStore -> List SmsOutbound -> DataStore
updateSmsOutbounds ds sms =
    { ds
        | outboundSms =
            mergeItems ds.outboundSms sms
                |> List.sortBy compareByTS
                |> List.reverse
    }


updateSmsInbounds : DataStore -> List SmsInbound -> DataStore
updateSmsInbounds ds newSms =
    { ds
        | inboundSms =
            mergeItems ds.inboundSms newSms
                |> sortByTimeReceived
    }


updateQueuedSms : DataStore -> List QueuedSms -> DataStore
updateQueuedSms ds newSms =
    { ds
        | queuedSms =
            mergeItems ds.queuedSms newSms
                |> List.sortBy compareByT2S
    }


updateKeywords : DataStore -> List Keyword -> DataStore
updateKeywords ds keywords =
    { ds | keywords = mergeItems ds.keywords keywords |> List.sortBy .keyword }


updateRecipients : DataStore -> List Recipient -> DataStore
updateRecipients dataStore newRecipients =
    { dataStore
        | recipients =
            mergeItems dataStore.recipients newRecipients
                |> List.sortBy .last_name
    }


updateGroups : DataStore -> List RecipientGroup -> DataStore
updateGroups ds groups =
    { ds
        | groups =
            mergeItems ds.groups groups
                |> List.sortBy .name
    }


updateUserProfiles : DataStore -> List UserProfile -> DataStore
updateUserProfiles dataStore profiles =
    { dataStore
        | userprofiles =
            mergeItems dataStore.userprofiles profiles
                |> List.sortBy (.email << .user)
    }


updateElvantoGroups : DataStore -> List ElvantoGroup -> DataStore
updateElvantoGroups ds newGroups =
    { ds
        | elvantoGroups =
            mergeItems ds.elvantoGroups newGroups
                |> List.sortBy .name
    }


optArchiveRecordWithPk : List { a | pk : Int, is_archived : Bool } -> Int -> List { a | pk : Int, is_archived : Bool }
optArchiveRecordWithPk recs pk =
    recs
        |> List.map (toggleIsArchived pk)


toggleIsArchived : Int -> { a | pk : Int, is_archived : Bool } -> { a | pk : Int, is_archived : Bool }
toggleIsArchived pk rec =
    case pk == rec.pk of
        True ->
            { rec | is_archived = not rec.is_archived }

        False ->
            rec



-- merge new items with existing


mergeItems : List { a | pk : Int } -> List { a | pk : Int } -> List { a | pk : Int }
mergeItems existingItems newItems =
    existingItems
        |> List.map (\x -> ( x.pk, x ))
        |> Dict.fromList
        |> addNewItems newItems
        |> Dict.values


addNewItems : List { a | pk : Int } -> Dict.Dict Int { a | pk : Int } -> Dict.Dict Int { a | pk : Int }
addNewItems newItems existingItemsDict =
    newItems
        |> List.foldl addItemToDic existingItemsDict


addItemToDic : { a | pk : Int } -> Dict.Dict Int { a | pk : Int } -> Dict.Dict Int { a | pk : Int }
addItemToDic item existingItems =
    Dict.insert item.pk item existingItems



-- Sorting


compareByTS : SmsOutbound -> Float
compareByTS sms =
    case sms.time_sent of
        Just d ->
            Date.toTime d

        Nothing ->
            toFloat 1


compareByT2S : { a | time_to_send : Maybe Date.Date } -> Float
compareByT2S sms =
    case sms.time_to_send of
        Just d ->
            Date.toTime d

        Nothing ->
            toFloat 1


sortByTimeReceived : List { a | time_received : Maybe Date.Date } -> List { a | time_received : Maybe Date.Date }
sortByTimeReceived items =
    items
        |> List.sortBy compareTR
        |> List.reverse


compareTR : { a | time_received : Maybe Date.Date } -> Float
compareTR item =
    case item.time_received of
        Just d ->
            Date.toTime d

        Nothing ->
            toFloat 1
