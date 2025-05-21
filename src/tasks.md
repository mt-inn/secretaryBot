# コマンド一覧
テスト済みのものにチェックを入れていく。


- [x] displayconfig
現在の設定とスケジュールの一覧を表示する
もうちょい見やすくしよう
- [ ] configremind
リマインドの送信先を設定する
DMに送信できない
- [x] configtalk
書き込みに反応する場所を設定する
- [ ] add_event
イベントを追加する。
予定追加できた
リマインドが来ない

- [ ] delete_event
イベントを削除する
できなかった

- [ ] update_event
イベントを編集する
できなかった

- [ ] list_events
イベントを一覧表示する
できなかった

- [ ] remind_after
任意の期間後にリマインドする
動かん

PS C:\Users\ocami\GitHub> & C:/Users/ocami/AppData/Local/Programs/Python/Python313/python.exe c:/Users/ocami/GitHub/secretaryBot/src/main.py
2025-05-21 15:09:40 INFO     discord.client logging in using static token
2025-05-21 15:09:41 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: 3cef6f08249d1bc6b34a1015ce0ccd51).
起動完了
Task exception was never retrieved
future: <Task finished name='Task-8' coro=<Reminder.start_reminder_loop.<locals>.checkLoop() done, defined at c:\Users\ocami\GitHub\secretaryBot\src\core\secretaryCalendarCore.py:197> exception=AttributeError("'NoneType' object has no attribute 'send'")>
Traceback (most recent call last):
  File "c:\Users\ocami\GitHub\secretaryBot\src\core\secretaryCalendarCore.py", line 206, in checkLoop
    await self._remind(event)
  File "c:\Users\ocami\GitHub\secretaryBot\src\core\secretaryCalendarCore.py", line 169, in _remind
    await self.sendMessage(content=text)
  File "c:\Users\ocami\GitHub\secretaryBot\src\core\secretaryCalendarCore.py", line 35, in sendMessage
    await self.addres.send(content)
          ^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'send'
2025-05-21 15:14:51 ERROR    discord.app_commands.tree Ignoring exception in command 'delete_event'
Traceback (most recent call last):
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 858, in _do_call      
    return await self._callback(interaction, **params)  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\ocami\GitHub\secretaryBot\src\main.py", line 126, in command_deleteEvent
    deleted = await rem.delete_event(name, dt)
                                           ^^
UnboundLocalError: cannot access local variable 'dt' where it is not associated with a value

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\tree.py", line 1310, in _call
    await command._invoke_with_namespace(interaction, namespace)
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 883, in _invoke_with_namespace
    return await self._do_call(interaction, transformed_values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 876, in _do_call      
    raise CommandInvokeError(self, e) from e
discord.app_commands.errors.CommandInvokeError: Command 'delete_event' raised an exception: UnboundLocalError: cannot access local variable 'dt' where it is not associated with a value
2025-05-21 15:16:48 ERROR    discord.app_commands.tree Ignoring exception in command 'update_event'
Traceback (most recent call last):
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 858, in _do_call      
    return await self._callback(interaction, **params)  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\ocami\GitHub\secretaryBot\src\main.py", line 164, in command_updateEvent
    a = await rem.update_event(old_name=old_name, old_date=str2dt(old_date), new_event_data=new_data)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: object bool can't be used in 'await' expression

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\tree.py", line 1310, in _call
    await command._invoke_with_namespace(interaction, namespace)
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 883, in _invoke_with_namespace
    return await self._do_call(interaction, transformed_values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 872, in _do_call      
    raise CommandInvokeError(self, e) from e
discord.app_commands.errors.CommandInvokeError: Command 'update_event' raised an exception: TypeError: object bool can't be used in 'await' expression
2025-05-21 15:17:15 ERROR    discord.app_commands.tree Ignoring exception in command 'list_events'
Traceback (most recent call last):
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 858, in _do_call      
    return await self._callback(interaction, **params)  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\ocami\GitHub\secretaryBot\src\main.py", line 193, in command_listEvents
    eventList = await rem.list_events(date=str2dt(date))
                                           ~~~~~~^^^^^^
  File "c:\Users\ocami\GitHub\secretaryBot\src\main.py", line 30, in str2dt
    while re.match(r'\D',text[-1]):
                         ~~~~^^^^
TypeError: 'NoneType' object is not subscriptable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\tree.py", line 1310, in _call
    await command._invoke_with_namespace(interaction, namespace)
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 883, in _invoke_with_namespace
    return await self._do_call(interaction, transformed_values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ocami\AppData\Local\Programs\Python\Python313\Lib\site-packages\discord\app_commands\commands.py", line 872, in _do_call      
    raise CommandInvokeError(self, e) from e
discord.app_commands.errors.CommandInvokeError: Command 'list_events' raised an exception: TypeError: 'NoneType' object is not subscriptable 