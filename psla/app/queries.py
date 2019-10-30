# -*- coding: utf-8 -*

""" These are the pre-configured SQL queries and graphs which are run
    by the code in routes.py
"""

graphs = [{'title': u'コマンドの最大同時実行数(１分刻み)',
           'id': 'cmds_per_minute',
           'graph_type': 'bar',
           'explanation': u'同時に実行されたコマンドの数の最大値を１分刻みでカウント',
           'x': {'title': 'Minute',
                 'field': 'Minute'},
           'y': {'title': 'Num Cmds',
                 'field': 'MaxCommands'},
           'sql': """
                SELECT SUBSTR(startTime, 0, 17) as 'Minute', MAX(running) as 'MaxCommands'
                FROM process
                GROUP BY Minute;
            """},
          {'title': u'開始されたコマンドの数(１０分刻み)',
           'id': 'cmds_per_10_minute',
           'graph_type': 'bar',
           'explanation': u'開始されたコマンドの数を１０分刻みでカウント',
           'x': {'title': 'Ten Minute',
                 'field': 'TenMinute'},
           'y': {'title': 'Num Cmds',
                 'field': 'NumCommands'},
           'sql': """
                        SELECT SUBSTR(startTime, 0, 16) as 'TenMinute', COUNT(cmd) as 'NumCommands'
                        FROM process
                        GROUP BY TenMinute;
                    """},
          {'title': u'実行されたコマンドの総数(タイプ別)',
            'id': 'cmd_totals',
            'graph_type': 'bar',
            'explanation': u'実行されたコマンドの数をタイプ別にカウント',
            'x': {'title': 'Cmd',
                 'field': 'Cmd'},
            'y': {'title': 'Num Cmds',
                 'field': 'NumCmds'},
            'sql': """
                select cmd as 'Cmd', count(cmd) as 'NumCmds'
                from process
                group by cmd
                order by NumCmds desc
                limit 15;
                """},
        {'title': u'実行されたコマンドの総数(ユーザ別)',
            'id': 'cmds_per_user',
            'graph_type': 'bar',
            'explanation': u'実行されたコマンドの数をユーザ別にカウント',
            'x': {'title': 'User',
                 'field': 'User'},
            'y': {'title': 'Num Cmds',
                 'field': 'NumCmds'},
            'sql': """
                select user as 'User', count(user) as 'NumCmds'
                from process
                group by user
                order by NumCmds desc
                limit 15;
                """}
          ]

queries = [{'title': u'タイムフレーム',
            'explanation': u'ログファイルの先頭時刻と終端時刻',
            'sql': """
                select MIN(starttime) as Start, MAX(starttime) as End
                from process;
            """},
           {'title': u'実行されたコマンドの総数(タイプ別)',
            'explanation': u'実行されたコマンドの数をタイプ別にカウント',
            'sql': """
                select cmd, count(cmd) as CountCmds from process
                group by cmd
                order by CountCmds desc limit 20;
            """},
           {'title': u'実行されたコマンドの総数(タイプ別＆ユーザ別)',
            'explanation': u'実行されたコマンドの数をタイプ別＆ユーザ別にカウント',
            'sql': """
                select cmd, count(cmd) as CountCmds, user 
                from process
                group by cmd, user
                order by CountCmds desc limit 30;
            """},
           {'title': u'平均待ち時間',
            'explanation': u'平均待ち時間',
            'sql': """
                SELECT AVG(totalreadWait+totalwriteWait) as wait
                FROM tableUse;
            """},

           {'title': u'ロックのきっかけを作ったユーザ',
            'explanation': u'ロックの引き金となったコマンドを実行したユーザ',
            'sql': """
                SELECT user, SUM(maxreadHeld+maxwriteHeld) as held
                FROM tableUse JOIN process USING (processKey)
                GROUP BY user ORDER BY held DESC LIMIT 25;
            """},

           {'title': u'ブロックの引き金となったコマンド(meta/client/changeテーブルを除く)',
            'explanation': u'他のコマンドをブロックしたコマンド(meta/client/changeテーブルを除く)',
            'sql': """
            	SELECT startTime, endTime, running, user, cmd, pid, tablename,
            	    maxReadHeld, maxWriteHeld, totalReadWait, totalWriteWait
                FROM tableUse JOIN process USING (processKey)
                WHERE (totalReadHeld > 10000 or totalWriteHeld > 10000)
                    AND tablename not like 'meta%'
                    AND tablename not like 'clients%'
                    AND tablename not like 'changes%'
                ORDER BY startTime, endTime
                    limit 30;
            """},

            {'title': u'ブロックの引き金となったコマンド(全てのテーブルが対象)',
            'explanation': u'他のコマンドをブロックしたコマンド(全てのテーブルが対象)',
            'sql': """
            	SELECT startTime, endTime, running, user, cmd, pid, tablename,
            	    maxReadHeld, maxWriteHeld, totalReadWait, totalWriteWait
                FROM tableUse JOIN process USING (processKey)
                WHERE (totalReadHeld > 10000 or totalWriteHeld > 10000)
                ORDER BY startTime, endTime
                    limit 30;
            """},

            {'title': u'ブロックの引き金となったコマンドとユーザ(全てのテーブルが対象)',
            'explanation': u'他のコマンドをブロックしたコマンドとユーザ(全てのテーブルが対象)',
            'sql': """
                SELECT startTime, endTime, computedLapse, running, user, cmd, pid, tablename,
                    maxReadHeld, maxWriteHeld,totalReadWait, totalWriteWait
                FROM tableUse JOIN process USING (processKey)
                WHERE (totalReadWait > 10000) or (totalWriteWait > 10000)
                ORDER BY startTime, endTime
                limit 30;
            """},

            {'title': u'計算フェーズの経過時間(トップ25)',
            'explanation': u'計算フェーズの経過時間が長いコマンド(トップ25)',
            'sql': """
                SELECT process.processKey, user, cmd, args, startTime,
                CASE WHEN MAX(totalreadHeld + totalwriteHeld) > MAX(totalreadWait + totalwriteWait) THEN
                    MAX(totalreadHeld + totalwriteHeld) - MAX(totalreadWait + totalwriteWait)
                ELSE
                    MAX(totalreadHeld + totalwriteHeld)
                END
                AS compute
                FROM tableUse JOIN process USING (processKey)
                GROUP BY tableUse.processKey
                ORDER BY compute DESC LIMIT 25
            """},

            {'title': u'I/Oアクセスの数(トップ25)',
            'explanation': u'I/Oアクセスが多いコマンド(トップ25)',
            'sql': """
                SELECT user, cmd, SUM(pagesIn+pagesOut) as io, process.processKey, process.args
                FROM tableUse JOIN process USING (processKey)
                GROUP BY tableUse.processKey ORDER BY io
                DESC LIMIT 25
            """},

            {'title': u'ページ読み込みとページ書き込みの割合',
            'explanation': u'ページ読み込みとページ書き込みの割合',
            'sql': """
                SELECT TOTAL(pagesIn) * 100.0 / (TOTAL(pagesIn)+TOTAL(pagesOut)) as readPct,
                    TOTAL(pagesOut) * 100.0 / (TOTAL(pagesIn)+TOTAL(pagesOut)) as writePct
                FROM tableUse
            """},
           {'title': u'システムCPUの使用率(トップ25)',
            'explanation': u'システムCPUの使用率が多いコマンド(トップ25)',
            'sql': """
                select pid, user, cmd, completedLapse, rpcRcv, rpcSnd, uCpu, sCpu, startTime, endTime
                from process 
                order by sCpu desc limit 25
            """},
           {'title': u'ユーザCPUの使用率(トップ25)',
            'explanation': u'ユーザCPUの使用率が多いコマンド(トップ25)',
            'sql': """
                select pid, user, cmd, completedLapse, rpcRcv, rpcSnd, uCpu, sCpu, startTime, endTime 
                from process 
                order by uCpu desc limit 25 
            """},

           # {'title': '',
           #  'explanation': '',
           #  'sql': """
           #  """},
           ]

