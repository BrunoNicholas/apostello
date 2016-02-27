import React, { Component } from 'react';
import post from './../ajax_post';
import { LoadingComponent } from './reloading_component';
import { FilteringComponent } from './filtering_component';
import UserProfileTableRow from './user_profile_row';

class UserProfilesTable extends Component {
  constructor() {
    super();
    this.postUpdate = this.postUpdate.bind(this);
  }
  postUpdate(user) {
    post(
      `/api/v1/users/profiles/${user.pk}`,
      { user_profile: JSON.stringify(user) },
      this.props.loadfromserver
    );
  }
  render() {
    const that = this;
    const rows = this.props.data.map(
      (user, index) => <UserProfileTableRow
        user={user}
        key={index}
        postUpdate={that.postUpdate}
      />
    );
    return (
      <table className="ui collapsing celled very basic table">
        <thead>
          <tr className="left aligned">
            <th>User</th>
            <th>Approved</th>
            <th>Keywords</th>
            <th>Send SMS</th>
            <th>Contacts</th>
            <th>Groups</th>
            <th>Incoming</th>
            <th>Outgoing</th>
          </tr>
        </thead>
        <tbody className="searchable">
          {rows}
        </tbody>
      </table>
    );
  }
}

export default LoadingComponent(FilteringComponent(UserProfilesTable));
