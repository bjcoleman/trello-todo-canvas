
## Trello TODO list from Canvas Courses

This repo contains code to generate TODO list items 
in Trello from assignments in Canvas courses.  When
executed, `main.py` will perform the following once per
hour:

* Read a list of courses from a local Redis DB
* Read a list of assignments for each course from Canvas
* For each assignment, if the due date is in the past
  and the assignment group does not contain "Ungraded",
  add the assignment to the Trello list if not already present
  
  
## Configuration

* Ensure [redis](https://redis.io/) is installed and
  the server is running
* Add all course ids to a set named `courses` in Redis
* Add assignment groups to skip to a set named `skip` in Redis.
  The format is <courseID>:<groupID>, e.g. "13514:30674"
* Create a Canvas Access Token from the Settings page on Canvas
* Create a [Trello Key and Token](https://trello.com/app-key)  
* Create a file `.env` in this folder that contains:

   ```
  CANVAS_TOKEN=<token>
  TRELLO_API_KEY=<key>
  TRELLO_TOKEN=<token>
  ```
 * Install required packages: `pip3 install -r requirements.txt`
 * Launch at boot via `screen`: Add the following to `/etc/rc.local`
   ```
   screen -dm python3 /trello-todo-canvas/main.py
   ```
   
   Edit to the proper directory, as necessary.
   