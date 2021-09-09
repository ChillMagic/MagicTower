/*
 *  Anex86: PC-x86 emulator 
 *    Copyright (C) 1998-2005 A.N. All rights reserved.
 *      anecdxnt.e86: v2.78
 *      cdx.sys:      v1.01
 */


[はじめに]

  　ダウンロード、ありがとうございました。
  Anecdx は Anex86 の追加モジュールのひとつで、エミュレータ内の MS-DOS から
  パソコンの CD-ROM へのアクセスを提供します。

    このパッケージには以下のファイルが含まれています。
        readme.txt     このファイルです。必ず読んでください。
        anecdxnt.e86   Anex86 用の追加モジュールです。
                       anex86.exe と同じディレクトリに置いてください。
                       anex86.exe と同じバージョンを使用してください。
        cdx.sys        Anex86 内の MS-DOS 用のデバイスドライバです。
                       実機では絶対に組み込まないでください。
                       実機に組み込んで何が起きても責任持ちません。


[必要なもの]

  ・このプログラムを使用するためには同じバージョンの Anex86 が必要です。
  　
  ・このプログラムは Anex86 内の MS-DOS のみサポートします。
  　
  ・MSCDEX.EXE が必要です。


[使い方]

  (1). anecdxnt.e86 を anex86.exe と同じディレクトリに置きます。
  (2). mscdex.exe/cdx.sys を Anex86 の .fdi か .hdi にコピーしておきます。
  (3). anex86.exe をダブルクリックして Anex86 を起動します。
  (4). [Config]-[CDX] タブを開きます。
  (5). ドライブを指定します。
       ドライブは Anex86 を実行するパソコンの CD-ROM です。
　　　　Anex86 内の MS-DOS の CD-ROM ドライブは MSCDEX で指定します。
  (6). Anex86 内の MS-DOS の CONFIG.SYS と AUTOEXEC.BAT を変更します。
       CONFIG.SYS の例（/D オプションは必須です。省略不可）
         LASTDRIVE=Z
         DEVICE=CDX.SYS /D:CD_101
       AUTOEXEC.BAT の例 
         MSCDEX /D:CD_101 /L:Q
  (7). [Start] を押して Anex86 内の MS-DOS を起動します。


  ※正常に組み込まれたかどうかは、[Config]-[Manager] で確認できます。

  ※Anex86 で使用するアプリケーションとその設定によっては、
    追加モジュールを使うと動くもの、逆に、動かなくなるもの、があります。
    （実機にカードやデバイスを追加したときと同じことです）

  ※最初は追加モジュール無しで試してみることをお勧めします。
    また、問題が生じたときは追加モジュールを外してみてください。


[制限事項]

  ・Anex86 内で MS-DOS 3.x-6.x が必要です。

  ・CD-ROM の挙動は Windows 側のドライバに依存します。
  　実行するマシンによって動作が異なる場合があります。


[重要]

  ・このモジュールはパソコンに影響を与える可能性があります。
  　何が起きても A.N. は一切責任を持ちません。


