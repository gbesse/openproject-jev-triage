# OpenProject Jev Triage

Experimental community alpha v0.1.4 · MIT.

## Français

Exemple hors ligne : `python3 examples/offline_decisions.py` rejoue « Ajouter un bouton export ; les critères et le responsable sont documentés. » avec une réponse synthétique à forte puis faible probabilité. La faible probabilité reste en revue ; aucune clé ni requête réseau.

Un service vérifie les webhooks OpenProject sur les nouveaux work packages, évalue la complétude de la demande et ajoute un commentaire de revue. Il ne modifie pas le statut.

Installation :

```sh
python3 app.py
```

Variables serveur : `TYPESAFE_API_KEY, OPENPROJECT_WEBHOOK_SECRET, OPENPROJECT_URL, OPENPROJECT_API_TOKEN`. Garder les secrets hors du dépôt et de la configuration visible par les utilisateurs.

Créer un webhook signé vers `/webhook` sur la création de work packages ; utiliser un compte API autorisé à ajouter des commentaires. Ne pas abonner ce service aux commentaires qu’il crée.

L’appel API utilise l’authentification Basic avec le nom `apikey`, compatible avec les versions d’OpenProject antérieures à la prise en charge des jetons Bearer. Les charges JSON invalides reçoivent une réponse 400.

Avant d’appeler Jev, le service lit les activités du work package et ignore une revue portant déjà le même texte et la même politique. Le compte API doit pouvoir lire ces activités. Des livraisons simultanées peuvent encore créer des commentaires en double.

## English

Offline example: `python3 examples/offline_decisions.py` replays “Add an export button; acceptance criteria and owner are documented.” with synthetic high and low probability responses. Low probability remains in review; no key or network request.

A service verifies OpenProject webhooks for new work packages, evaluates request completeness, and adds a review comment. It does not change status.

Setup:

```sh
python3 app.py
```

Server variables: `TYPESAFE_API_KEY, OPENPROJECT_WEBHOOK_SECRET, OPENPROJECT_URL, OPENPROJECT_API_TOKEN`. Keep secrets outside the repository and user-visible configuration.

Create a signed webhook to `/webhook` for work package creation; use an API account allowed to add comments. Do not subscribe the service to comments it creates.

The API call uses Basic authentication with the `apikey` username, compatible with OpenProject versions predating Bearer token support. Invalid JSON payloads receive a 400 response.

Before calling Jev, the service reads work package activities and skips a review with the same text and policy. The API account must be able to read these activities. Concurrent deliveries can still create duplicate comments.

## Español

Ejemplo sin conexión: `python3 examples/offline_decisions.py` reproduce «Añadir un botón de exportación; los criterios y el responsable están documentados.» con respuestas sintéticas de probabilidad alta y baja. La probabilidad baja queda para revisión; no requiere clave ni red.

Un servicio verifica webhooks de OpenProject para nuevos paquetes de trabajo, evalúa si la solicitud está completa y añade un comentario de revisión. No cambia el estado.

Instalación:

```sh
python3 app.py
```

Variables del servidor: `TYPESAFE_API_KEY, OPENPROJECT_WEBHOOK_SECRET, OPENPROJECT_URL, OPENPROJECT_API_TOKEN`. Mantén los secretos fuera del repositorio y de la configuración visible para usuarios.

Crea un webhook firmado hacia `/webhook` para la creación de paquetes de trabajo; usa una cuenta API autorizada a comentar. No suscribas el servicio a los comentarios que crea.

La llamada API usa autenticación Basic con el usuario `apikey`, compatible con versiones de OpenProject anteriores a la compatibilidad con tokens Bearer. Las cargas JSON inválidas reciben una respuesta 400.

Antes de llamar a Jev, el servicio lee las actividades del paquete de trabajo y omite una revisión del mismo texto y política. La cuenta API debe poder leer esas actividades. Las entregas simultáneas aún pueden crear comentarios duplicados.

## Verification / Vérification / Verificación

```sh
python3 -m unittest discover -s tests -v
```

Tests use synthetic Jev responses and host event fixtures. Threshold `0.9` in `policy.json` is an example and must be calibrated on labeled data before automatic actions. No live host or Jev service has been exercised. / Les tests utilisent des réponses synthétiques et le seuil doit être calibré ; aucun hôte ni service Jev réel n’a été testé. / Las pruebas usan respuestas sintéticas y el umbral debe calibrarse; no se ha probado un host ni un servicio Jev real.

Host reference / Référence de l’hôte / Referencia del host: https://www.openproject.org/docs/system-admin-guide/api-and-webhooks/

The receiver listens on `127.0.0.1:8080` by default; use a TLS reverse proxy for remote webhooks. `LISTEN_HOST` and `PORT` can override the bind address. / Le service écoute par défaut sur `127.0.0.1:8080` ; utiliser un proxy TLS pour les webhooks distants. / El servicio escucha por defecto en `127.0.0.1:8080`; usa un proxy TLS para webhooks remotos.

## October 2026 improvement · Amélioration d’octobre 2026 · Mejora de octubre de 2026

Run `python3 examples/provenance_edit.py` to see that editing a work-package text changes its input hash, using synthetic responses only.

Exécutez `python3 examples/provenance_edit.py` pour voir qu’une modification du texte d’un ticket change son empreinte d’entrée, avec des réponses synthétiques seulement.

Ejecute `python3 examples/provenance_edit.py` para ver que editar el texto de una tarea cambia su huella de entrada, usando solo respuestas sintéticas.
