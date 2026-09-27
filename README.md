# OpenProject Jev Triage

Experimental community alpha v0.1.0 · MIT.

## Français

Un service vérifie les webhooks OpenProject sur les nouveaux work packages, évalue la complétude de la demande et ajoute un commentaire de revue. Il ne modifie pas le statut.

Installation :

```sh
python3 app.py
```

Variables serveur : `TYPESAFE_API_KEY, OPENPROJECT_WEBHOOK_SECRET, OPENPROJECT_URL, OPENPROJECT_API_TOKEN`. Garder les secrets hors du dépôt et de la configuration visible par les utilisateurs.

Créer un webhook signé vers `/webhook` sur la création de work packages ; utiliser un compte API autorisé à ajouter des commentaires. Ne pas abonner ce service aux commentaires qu’il crée.

## English

A service verifies OpenProject webhooks for new work packages, evaluates request completeness, and adds a review comment. It does not change status.

Setup:

```sh
python3 app.py
```

Server variables: `TYPESAFE_API_KEY, OPENPROJECT_WEBHOOK_SECRET, OPENPROJECT_URL, OPENPROJECT_API_TOKEN`. Keep secrets outside the repository and user-visible configuration.

Create a signed webhook to `/webhook` for work package creation; use an API account allowed to add comments. Do not subscribe the service to comments it creates.

## Español

Un servicio verifica webhooks de OpenProject para nuevos paquetes de trabajo, evalúa si la solicitud está completa y añade un comentario de revisión. No cambia el estado.

Instalación:

```sh
python3 app.py
```

Variables del servidor: `TYPESAFE_API_KEY, OPENPROJECT_WEBHOOK_SECRET, OPENPROJECT_URL, OPENPROJECT_API_TOKEN`. Mantén los secretos fuera del repositorio y de la configuración visible para usuarios.

Crea un webhook firmado hacia `/webhook` para la creación de paquetes de trabajo; usa una cuenta API autorizada a comentar. No suscribas el servicio a los comentarios que crea.

## Verification / Vérification / Verificación

```sh
python3 -m unittest discover -s tests -v
```

Tests use synthetic Jev responses and host event fixtures. Threshold `0.9` in `policy.json` is an example and must be calibrated on labeled data before automatic actions. No live host or Jev service has been exercised. / Les tests utilisent des réponses synthétiques et le seuil doit être calibré ; aucun hôte ni service Jev réel n’a été testé. / Las pruebas usan respuestas sintéticas y el umbral debe calibrarse; no se ha probado un host ni un servicio Jev real.

Host reference / Référence de l’hôte / Referencia del host: https://www.openproject.org/docs/system-admin-guide/api-and-webhooks/

The receiver listens on `127.0.0.1:8080` by default; use a TLS reverse proxy for remote webhooks. `LISTEN_HOST` and `PORT` can override the bind address. / Le service écoute par défaut sur `127.0.0.1:8080` ; utiliser un proxy TLS pour les webhooks distants. / El servicio escucha por defecto en `127.0.0.1:8080`; usa un proxy TLS para webhooks remotos.
