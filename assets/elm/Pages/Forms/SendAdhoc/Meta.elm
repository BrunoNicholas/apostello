module Pages.Forms.SendAdhoc.Meta exposing (meta)

import Forms.Model exposing (FieldMeta)


meta : { content : FieldMeta, recipients : FieldMeta, scheduled_time : FieldMeta }
meta =
    { content = FieldMeta True "id_content" "content" "Content" Nothing
    , recipients = FieldMeta True "id_recipients" "recipients" "Recipients" Nothing
    , scheduled_time = FieldMeta False "id_scheduled_time" "scheduled_time" "Scheduled Time" (Just "Leave this blank to send your message immediately, otherwise select a date and time to schedule your message")
    }
