import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: [ './message.component.css' ]
})
export class MessageComponent implements OnInit {

  pageTitle: string = 'List of messages';

  messages = [
    {
      "id": 1,
      "channel": {
        "title": "Test Channel",
        "username": "@tcms_test",
        "bot": "http://localhost:8000/api/bots/526520643/"
      },
      "text": "Text",
      "image": null,
      "send_time": "2018-02-28T22:14:54Z"
    },
    {
      "id": 2,
      "channel": {
        "title": "Test Channel",
        "username": "@tcms_test",
        "bot": "http://localhost:8000/api/bots/526520643/"
      },
      "text": null,
      "image": "http://localhost:8000/static/img/13714_4pWBkCa.jpg",
      "send_time": "2018-02-28T15:04:03Z"
    },
    {
      "id": 3,
      "channel": {
        "title": "IT уголовные дела СОРМ россиюшка",
        "username": "@unkn0wnerror",
        "bot": "http://localhost:8000/api/bots/526520643/"
      },
      "text": "E",
      "image": null,
      "send_time": "2018-03-01T00:11:32Z"
    }
  ]

  constructor() {
  }

  ngOnInit() {
  }

}
