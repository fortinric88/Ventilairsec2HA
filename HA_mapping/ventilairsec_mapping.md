Table de mapping proposé — Ventilairsec (VMI) Jeedom -> Home Assistant

But: LogicalId Jeedom -> Entité Home Assistant (proposition)

Sensors (lecture)
- `IEFIL::value` -> `sensor.ventilairsec_filter` (pourcentage)
- `CVITM::raw_value` -> `sensor.ventilairsec_motor_speed` (consigne vitesse moteur)
- `TEMP0::value` -> `sensor.ventilairsec_temp0`
- `TEMP1::value` -> `sensor.ventilairsec_temp1`
- `TEMP2::value` -> `sensor.ventilairsec_temp2`
- `TEMP3::value` -> `sensor.ventilairsec_temp3`
- `TEMP4::value` -> `sensor.ventilairsec_temp4`
- `HUM0::value` -> `sensor.ventilairsec_hum0`
- `HUM1::value` -> `sensor.ventilairsec_hum1`
- `HUM2::value` -> `sensor.ventilairsec_hum2`
- `HUM3::value` -> `sensor.ventilairsec_hum3`
- `HUM4::value` -> `sensor.ventilairsec_hum4`
- `POS0::value` -> `sensor.ventilairsec_probe0_pos` (string)
- `POS1::value` -> `sensor.ventilairsec_probe1_pos`
- `POS2::value` -> `sensor.ventilairsec_probe2_pos`
- `POS3::value` -> `sensor.ventilairsec_probe3_pos`
- `POS4::value` -> `sensor.ventilairsec_probe4_pos`
- `MF::raw_value` -> `sensor.ventilairsec_modefonc` (valeur interne)
- `ETATS::value` -> `sensor.ventilairsec_state` (texte / status)
- `PLH::raw_value` -> `sensor.ventilairsec_plage` (plage horaire active - binaire/flags)
- `DEBF::raw_value` -> `sensor.ventilairsec_debit_fixe` (binaire)
- `SURV::raw_value` -> `sensor.ventilairsec_surventilation` (binaire)
- `VAC::raw_value` -> `sensor.ventilairsec_vacances` (binaire)
- `BOOS::raw_value` -> `sensor.ventilairsec_boost` (binaire ou intensité)
- `TEMPCELEC::value` -> `sensor.ventilairsec_temp_consig_elec`
- `TEMPMSOUFFL::value` -> `sensor.ventilairsec_temp_max_soufflage`
- `TEMPCHYDROR::value` -> `sensor.ventilairsec_temp_hydror`
- `TEMPCSOLAR::value` -> `sensor.ventilairsec_temp_solar`
- `SAIS::raw_value` -> `sensor.ventilairsec_saison` (numeric / enum)
- `DEBAS::value` -> `sensor.ventilairsec_debit_air_m3h`
- `PCHAUFF::value` -> `sensor.ventilairsec_puissance_chauffage`
- `CVITM::raw_value` -> `sensor.ventilairsec_consigne_vitesse` (déjà listé)
- `TEMPEXT::value` -> `sensor.ventilairsec_temp_exterieure`
- `CPDIFF::value` -> `sensor.ventilairsec_consigne_pression_diff`
- `NBSDMAINT::value` -> `sensor.ventilairsec_weeks_since_maintenance`
- `DFONC::value` -> `sensor.ventilairsec_run_days`
- `CERR1::value` -> `sensor.ventilairsec_error1` (hex / code)
- `CERR2::value` -> `sensor.ventilairsec_error2`
- `BYPAMO::raw_value` -> `sensor.ventilairsec_bypass_amont_present` (binaire)
- `VVENT::value` -> `sensor.ventilairsec_volume_m3`
- `VLOG::value` -> `sensor.ventilairsec_fw_version`
- `CAPTEUR0::value` .. `CAPTEUR9::value` -> `sensor.ventilairsec_capteur_N_info` (string), + automatisation : créer entités pour capteurs liés (temp/hum/co2) via leur `logicalId` openenocean
- `OUVHYDR::value` -> `sensor.ventilairsec_hydror_ouverture`
- `BYP::value` -> `sensor.ventilairsec_bypass_type`
- `OUVBY1::value` `OUVBY2::value` `OUVBY3::value` -> `sensor.ventilairsec_bypass_ouverture_1/2/3`
- `POSBY1::value` `POSBY2::value` `POSBY3::value` -> `sensor.ventilairsec_bypass_type_1/2/3`
- `dBm` -> `sensor.ventilairsec_signal_dbm`

Actions / Contrôles (services ou entités actionnables)
- `MSC:1,command:0,BOOST:#slider#` -> service `ventilairsec_enocean.set_boost` (ou `number.boost`) : envoie la valeur boost
- `MSC:1,command:0,VACS:#slider#` -> service `ventilairsec_enocean.set_vacances`
- `MSC:1,command:0,MODEFONC:#slider#` -> service `ventilairsec_enocean.set_modefonc`
- `MSC:1,command:0,FONC:#message#` -> service `ventilairsec_enocean.set_fonc` (utilisé pour `surventilation`, `debit`, `bypass`, `plage`) — payload construit comme dans `sendAction`
- `MSC:1,command:0,COMMAND:#slider#` -> service `ventilairsec_enocean.raz_filtre` (reset filtre)
- `MSC:1,command:0,TEMPEL:#slider#` -> service `ventilairsec_enocean.set_temp_preh` (pré-chauffage)
- `MSC:1,command:0,TEMPSOUF:#slider#` -> service `ventilairsec_enocean.set_temps_soufflage`
- `MSC:1,command:0,TEMPHYD:#slider#` -> service `ventilairsec_enocean.set_temp_hydro`
- `MSC:1,command:0,TEMPSOL:#slider#` -> service `ventilairsec_enocean.set_temp_solar`
- `MSC:1,command:1,HOUR:#message#` -> service `ventilairsec_enocean.send_hour` (envoi de l'heure)
- `MSC:1,command:2,AGENDA:#message#` -> service `ventilairsec_enocean.set_agenda` (envoi trames agenda)

Capteurs externes (openenocean)
- Les entrées `CAPTEURn::value` contiennent "id|room|profile". Pour chaque capteur référencé, l'intégration HA doit créer des `sensor`s correspondant aux commandes exposées par l'équipement `openenocean` (ex: `TMP::value`, `HUM::value`, `CONC::value` ou `CO2::value`). Exemple :
  - Si `CAPTEUR3::value` == `A1B2C3|Cuisine|A5_09_04` alors créer :
    - `sensor.capteur_cuisine_temperature` <- lecture `TMP::value` du device `A1B2C3`
    - `sensor.capteur_cuisine_humidity` <- `HUM::value`
    - `sensor.capteur_cuisine_co2` <- `CONC::value`

Remarques d'implémentation
- Le démon `openenoceand` échange des messages JSON sur un socket local (par défaut `127.0.0.1:55006`). L'intégration HA devra envoyer des JSON identiques à ce que Jeedom envoie (ex: `{"apikey":"<key>","cmd":"send","device":...,"message":...}`) afin que `openenoceand` relaie la commande.
- Pour une première version, je propose d'exposer :
  - un groupe de `sensor.*` pour tous les champs listés dans `$csvCmds` (lecture seule)
  - des `services` (namespace `ventilairsec_enocean`) pour les actions MSC (boost, vacances, fonc, debit, bypass, razfiltre, set_hour, set_agenda). Ces services construiront les trames comme dans `ventilairsec::sendAction` et enverront via TCP au démon.
- Gestion automatique des capteurs OpenEnocean : l'intégration lira `CAPTEURn::value` et créera dynamiquement les sensors correspondants en se basant sur le type/profile.

Prochaine étape : générer automatiquement un fichier `mapping.json` utilisable par l'intégration pour créer les entités (voulez-vous que je le fasse ?)