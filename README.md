Adding dialogs to your Flask Slack app
---------------------------------------

If you've ever build a Slack app which takes in user inputs in the form of messages, button clicks 
or message menu selections, you probably know how tricky it can be to correlate all of those 
selections in a form-like collection.

We're making these types of scenarios much easier by providing developers with Message Dialogs.

Message Dialogs
----------------

Dialogs are collections of arranged form elements. Users trigger your app's dialogs by clicking on buttons, selecting from menus, or invoking slash commands.

![dialog_demo v1506551505](https://user-images.githubusercontent.com/32463/30974229-01bcc2aa-a424-11e7-8a8c-51379efb70c2.gif)

While Message Buttons are a great way to increase the usability of your Slack application, there are some limitations. One limitation is the amount of real estate buttons take up. When you have a large set of options, you'll end up with a message that takes up the user's entire chat window or gets truncated.

Presented to users within a modal window, dialogs provide a focused workflow to quickly collect information from users.

Conversation with bots is best when it's casual, as natural as spoken language. If you need more structured information from a user, a straight forward form-based approach will lead to clear and actionable information.


See our [Dialogs documentation](https://api.slack.com/dialogs) for more information on dialogs.


Adding dialogs to your app
--------------------------------

In this tutorial, we'll focus on dialogs triggered by a button click, but dialogs may be triggered 
by selecting from a menu or invoking a slack command.


Here's a summary of dialog workflow:

1. Post a message containing a button for the user to begin the workflow, the button attachment JSON 
contains a ``callback_id``
2. When the user clicks the button, Slack sends you app the action event containing a ``trigger_id``
3. You app calls ``dialog.open``, passing the ``trigger_id`` and any form elements you want to display
4. Users fill out the dialog elements and submit
5. Your app receives an action event containing all the context you need to understand: who clicked it, 
which option they clicked, which message ``callback_id`` was associated with the message, and the original message inciting the selection
6. You respond to this action event with a message to replace the original, post a new ephemeral message, or you utilize the action's ``response_url`` to update the original message out of band for a limited time.


:bulb: The code is also available as a complete example application at [GitHub](https://github.com/slackapi/python-dialog-example/blob/master/example.py).


Support
--------

Need help? Join [Bot Developer Hangout](http://dev4slack.xoxco.com/) and talk to us in [#slack-api](https://dev4slack.slack.com/messages/slack-api/).


You can also create an Issue right here on [GitHub](https://github.com/slackapi/python-message-menu-example/issues).
