### Managed Software Update Localizable.strings

Password dialog for FileVault authorized restarts

![](https://github.com/munki/munki/wiki/images/auth_restart_dialog.png)

```
    /* Password prompt title */
        da: Managed Software Center skal låse startdisken op efter genstart for at færdiggøre alle ventende opdateringer.
        de: Die geführte Softwareaktualisierung möchte nach einem Neustart das Startvolume entsperren, um alle anstehenden Aktualisierungen abzuschließen.
        en: Managed Software Center wants to unlock the startup disk after restarting to complete all pending updates.
        es: Centro de Aplicaciones quiere desbloquear el disco de inicio tras el reinicio para completar todas las actualizaciones pendientes.
        fi: Managed Software Center haluaa avata käynnistyslevyn lukituksen seuraavalla käynnistyskerralla jatkaakseen päivitysten asentamista.
        fr: Le Centre de gestion des logiciels doit déverrouiller votre disque de démarrage au prochain redémarrage afin de terminer les mises à jour en attente.
        it: Centro Gestione Applicazioni vuole sbloccare il disco di avvio dopo il riavvio per completare gli aggiornamenti in sospeso.
        ja: Managed Software Centerは、すべての保留中のアップデートを完了させるため、再起動後、スタートアップディスクをアンロックします。
        nb: Managed Software Center vil låse startdisken opp etter omstart får å ferdigjøre alle ventende oppdateringer.
        nl: Managed Software Center wil de opstartschijf ontgrendelen na herstart zodat alle nog wachtende updates uitgevoerd kunnen worden.
        pt_BR: O Centro de Aplicativos Gerenciado quer desbloquear o disco de início depois de reiniciar para completar todos as atualizações pendentes.
        ru: Центр Управления ПО хочет разблокировать загрузочный диск после перезапуска, чтобы завершить все ожидающие обновления.
        sv: Managed Software Center behöver låsa upp startskivan efter omstart för att slutföra alla uppdateringar.
        
    /* Password explanation */
        da: For at tillade dette, skal du skrive din log ind-adgangskode.
        de: Bitte geben Sie Ihr Anmeldekennwort ein, um dies zu ermöglichen.
        en: To allow this, enter your login password.
        es: Para permitir esto, introduzca su contraseña de usuario.
        fi: Salli lukituksen avaaminen syöttämällä salasana.
        fr: Pour autoriser cette opération, veuillez entrer votre mot de passe.
        it: Per permettere questo, inserire la password di login.
        ja: これを許可する為、ログインパスワードを入力して下さい。
        nb: For å tillate dette, må du skrive inn ditt påloggingspassord.
        nl: Om dit toe te staan, vul je loginwachtwoord in.
        pt_BR: Para permitir isso, insira sua senha de login.
        ru: Для разрешения  введите свой пароль для входа в систему.
        sv: Ange ditt inloggningslösenord för att tillåta detta.

    /* Password label */ (ja and ru only)
        en: Password:
        it: Password:
        ja: パスワード:
        pt_BR: Senha:
        ru: Пароль:
        
    /* Allow button text */ (ja and ru only)
        en: Allow
        it: Consenti
        ja: 許可
        pt_BR: Permitir
        ru: Разрешить

    /* Deny button text */ (ja and ru only)
        en: Deny
        it: Rifiuta
        ja: 不許可
        pt_BR: Rejeitar
        ru: Не разрешать
```

### MunkiStatus Localizable.strings

Status messages for macOS upgrade installs
```
    /* managedsoftwareupdate message */
        da: Starter macOS-opgradering...
        de: macOS Upgrade wird gestartet...
        en: Starting macOS upgrade...
        es: Comenzando actualización de macOS...
        fi: Aloitetaan macOS-päivitystä...
        fr: La mise à jour de macOS démarre...
        it: Inizio aggiornamento macOS...
        ja: macOSアップグレードの開始...
        nb: Starter macOS-oppgradering...
        nl: Beginnen met macOS upgrade...
        pt_BR: Iniciando atualização do macOS...
        ru: Запуск обновление для macOS...
        sv: Påbörjar macOS-uppgradering...

    /* managedsoftwareupdate message */
        da: Forbereder afvikling af macOS-installeringsprogrammet...
        de: Das Ausführen der macOS Installation wird vorbereitet...
        en: Preparing to run macOS Installer...
        es: Preparando la ejecución del instalador de macOS...
        fi: Valmistaudutaan käynnistämään macOS-asentaja...
        fr: Installation de macOS en cours de préparation...
        it: Preparazione all'avvio di macOS Installer...
        ja: macOSインストーラーの実行を準備中...
        nb: Forbereder å kjøre macOS-installeringsprogrammet...
        nl: MacOS installatieprogramma voorbereiden...
        pt_BR: Preparando para executar a instalação do macOS...
        ru: Пoдготовка запуска Программы Установки macOS...
        sv: Förbereder macOS-installeraren...

    /* managedsoftwareupdate message */
        da: Systemet vil genstarte og begynde opgradering af macOS.
        de: Das System wird neu gestartet und die Aktualisierung von macOS begonnen.
        en: System will restart and begin upgrade of macOS.
        es: El sistema se reiniciará y comenzará la actualización de macOS.
        fi: Tietokone käynnistyy uudelleen ja aloittaa macOS-päivityksen.
        fr: Le système va redémarrer et commencer la mise à jour de macOS.
        it: Il sistema si riavvierà e inizierà l'aggiornamento di macOS.
        ja: システムを再起動し、macOSアップグレードを開始します。
        nb: Systemet vil gjøre en omstart og begynne oppgraderingen av macOS.
        nl: Systeem zal herstarten en de upgrade van macOS starten.
        pt_BR: O sistema irá reiniciar e começar a atualização do macOS.
        ru: Система перегрузится и начнет обновление macOS.
        sv: Datorn kommer att starta om och börja uppgradera macOS.
```