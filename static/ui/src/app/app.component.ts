import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: [ './app.component.css' ]
})
export class AppComponent {

  pageTitle: string = 'List of messages';

  messages = [
    {
      "id": 1,
      "channel": -1001199518653,
      "text": "Text",
      "image": null,
      "send_time": "2018-02-28T22:14:54Z"
    },
    {
      "id": 2,
      "channel": -1001199518653,
      "text": null,
      "image": "http://localhost:8000/api/messages/13714_4pWBkCa.jpg",
      "send_time": "2018-02-28T15:04:03Z"
    },
    {
      "id": 3,
      "channel": -1001037756687,
      "text": "E",
      "image": null,
      "send_time": "2018-03-01T00:11:32Z"
    }
  ]
}
