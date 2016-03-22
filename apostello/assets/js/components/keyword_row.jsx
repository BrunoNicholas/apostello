import React from 'react';
import KeywordStatus from './keyword_status';
import ArchiveButton from './archive_button';

const KeywordRow = (props) => (
  <tr>
    <td>
      <a href={props.keyword.url}>{props.keyword.keyword}</a>
    </td>
    <td>{props.keyword.description}</td>
    <td>{props.keyword.current_response}</td>
    <td>
      <a href={props.keyword.responses_url}>
        {props.keyword.num_replies}
      </a>
    </td>
    <td>
      <KeywordStatus is_live={props.keyword.is_live} />
    </td>
    <td>
      <ArchiveButton
        item={props.keyword}
        archiveFn={props.archiveKeyword}
      />
    </td>
  </tr>
);

export default KeywordRow;
