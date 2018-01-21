module Main exposing (main)

import Json.Decode as Decode
import Messages exposing (Msg(UrlChange))
import Models exposing (Model, decodeFlags, initialModel)
import Navigation
import Route exposing (loc2Page)
import Subscriptions exposing (subscriptions)
import Update exposing (update)
import View exposing (view)


main : Program Decode.Value Model Msg
main =
    Navigation.programWithFlags UrlChange
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


init : Decode.Value -> Navigation.Location -> ( Model, Cmd Msg )
init flagsVal location =
    let
        flags =
            case Decode.decodeValue decodeFlags flagsVal of
                Ok f ->
                    f

                Err msg ->
                    Debug.crash <| "Try reloading the page\n" ++ msg

        ( page, _ ) =
            loc2Page location flags.settings
    in
    page
        |> initialModel flags.settings
        |> update (UrlChange location)
