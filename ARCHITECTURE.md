# Architecture Idéale de HacxGPT

Cette architecture propose une réorganisation conceptuelle des composants de HacxGPT pour améliorer la modularité, l'extensibilité et la maintenabilité, sans modifier le code source actuel. Elle vise à séparer clairement les responsabilités et à faciliter l'intégration de nouvelles fonctionnalités et outils.

## 1. Noyau du Système (Core)

Le cœur du système, responsable de la logique principale de l'agent.

*   **`main.py` (ou `app.py`)**: Point d'entrée de l'application. Gère l'initialisation, le démarrage de l'interface utilisateur et la boucle principale de l'application.
    *   Gestion des arguments de ligne de commande (si applicable).
    *   Initialisation de `Config`, `UI`, `AgentCore`.
    *   Boucle principale du menu et de l'interaction utilisateur.
*   **`config.py`**: Centralise toutes les configurations et constantes du système.
    *   Paramètres de l'API (fournisseurs, modèles, URLs).
    *   Chemins de fichiers (environnement, logs).
    *   Thèmes, couleurs.
    *   Clés API (noms des variables d'environnement).
*   **`dependencies.py`**: Module dédié à la vérification et à l'installation des dépendances Python.
    *   `check_dependencies()`: Vérifie si les paquets nécessaires sont installés et les installe si ce n'est pas le cas.
    *   Gère le redémarrage du script après installation.

## 2. Interface Utilisateur (UI Layer)

Responsable de toutes les interactions avec l'utilisateur via le terminal.

*   **`ui.py`**: Classe `UI` gérant l'affichage, la saisie et la présentation des informations.
    *   `clear()`, `banner()`, `main_menu()`.
    *   `show_msg()`, `get_input()`.
    *   `stream_markdown()`: Gestion de l'affichage des réponses du LLM en streaming.
    *   Utilise `rich` pour un rendu avancé.

## 3. Moteur de l'Agent (Agent Engine)

Le cerveau de HacxGPT, encapsulant la logique d'interaction avec le LLM et la gestion des outils.

*   **`agent_core.py`**: Classe `AgentCore` (anciennement `HacxBrain`).
    *   Initialisation du client LLM (OpenAI, etc.).
    *   Gestion de l'historique de la conversation (`self.history`).
    *   `SYSTEM_PROMPT`: Le manifeste qui définit le comportement de l'agent.
    *   `chat()`: Méthode principale pour interagir avec le LLM, gérer les appels d'outils et le streaming des réponses.
    *   `reset()`: Réinitialise l'historique de la conversation.
    *   **Intégration et Orchestration des Outils**:
        *   `tool_manager.py` (voir ci-dessous).
        *   `_build_tools_schema()`: Génère le schéma des outils pour le LLM.
        *   `_execute_tool()`: Exécute un outil via le `ToolManager`.

## 4. Gestion des Outils (Tooling Layer)

Centralise la définition, l'enregistrement et l'exécution de tous les outils disponibles pour l'agent.

*   **`tool_manager.py`**: Classe `ToolManager`.
    *   Un registre interne pour tous les outils disponibles.
    *   Méthodes pour enregistrer de nouveaux outils.
    *   Méthode `execute_tool(tool_name, arguments)`: Prend le nom de l'outil et ses arguments, puis exécute l'outil correspondant. Gère les erreurs d'exécution.
    *   Potentiellement, une couche d'analyse post-exécution pour interpréter les résultats des outils avant de les renvoyer au LLM.
*   **`tools/` (Répertoire)**: Contient toutes les définitions des outils.
    *   Chaque outil est une classe distincte héritant d'une classe de base `BaseTool`.
    *   **`base_tool.py`**: Classe abstraite `BaseTool`.
        *   Définit l'interface commune pour tous les outils (ex: `description`, `parameters`, `execute`).
        *   Assure la cohérence des outils pour la génération du schéma OpenAI.
    *   **`tools/read.py`**, **`tools/write.py`**, **`tools/bash.py`**, etc.: Implémentations spécifiques de chaque outil.
        *   Chaque fichier contient une classe d'outil (ex: `ReadTool`, `WriteTool`, `BashTool`).
        *   Ces classes encapsulent la logique d'appel aux fonctions de l'API `default_api` fournie.

## 5. Gestion des Clés Secrètes (Secrets Management)

*   **`secrets.py`**: Module dédié à la gestion sécurisée des clés API et autres secrets.
    *   `load_api_key()`: Charge la clé API depuis le `.env`.
    *   `save_api_key()`: Sauvegarde la clé API dans le `.env` (avec `pwinput` pour la saisie masquée).
    *   Potentiellement, des fonctions pour gérer d'autres types de secrets (ex: identifiants SSH, clés de chiffrement) de manière plus robuste (chiffrement, gestion de vaults simples).

## 6. Schéma Hiérarchique des Modules

```
.
├── main.py                     # Point d'entrée de l'application
├── config.py                   # Configuration globale et constantes
├── dependencies.py             # Gestion des dépendances Python
├── ui.py                       # Couche d'interface utilisateur (Rich TUI)
├── agent_core.py               # Moteur principal de l'agent (ex-HacxBrain)
│   ├── SYSTEM_PROMPT           # Manifeste du comportement de l'agent
│   └── tool_manager.py         # Gestionnaire centralisé des outils
└── secrets.py                  # Gestion sécurisée des clés API et secrets
└── tools/                      # Répertoire des définitions d'outils
    ├── base_tool.py            # Classe abstraite de base pour tous les outils
    ├── read.py                 # Outil de lecture de fichiers
    ├── write.py                # Outil d'écriture de fichiers
    ├── edit.py                 # Outil d'édition de fichiers
    ├── bash.py                 # Outil d'exécution de commandes shell
    ├── file_finder.py          # Outil de recherche de fichiers
    ├── grep.py                 # Outil de recherche de texte dans les fichiers
    ├── network.py              # Outil de scan réseau (nmap, ping)
    ├── web.py                  # Outil de requêtes web (GET, POST)
    ├── crypto.py               # Outil de fonctions cryptographiques
    ├── disassembly.py          # Outil d'analyse binaire (désassemblage)
    └── file_analysis.py        # Outil d'analyse de fichiers (hashes, strings)
```

## Flux d'Exécution Remarqué

1.  **Démarrage**: `main.py` lance `check_dependencies()`.
2.  **Configuration**: `main.py` initialise `Config` et tente de charger la clé API via `secrets.py`. Si manquante, `ui.py` est utilisé pour la demander et `secrets.py` la sauvegarde.
3.  **Initialisation de l'Agent**: `main.py` crée une instance de `AgentCore`, qui à son tour initialise le client LLM et le `ToolManager` avec tous les outils disponibles dans `tools/`.
4.  **Boucle de Conversation**: `main.py` entre dans la boucle `run_chat()`.
    *   L'utilisateur entre une commande via `ui.py`.
    *   `AgentCore.chat()` est appelée avec l'entrée utilisateur.
    *   Le LLM génère une réponse. Si un appel d'outil est détecté :
        *   `AgentCore` demande à `ToolManager.execute_tool()` d'exécuter l'outil.
        *   `ToolManager` trouve et exécute l'outil approprié (ex: `BashTool.execute()`).
        *   Le résultat de l'outil est renvoyé à `AgentCore`, puis au LLM pour la suite de la conversation.
    *   La réponse finale (ou le streaming) du LLM est affichée via `ui.py`.

Cette structure permet une séparation claire des préoccupations, rendant le système plus robuste et plus facile à faire évoluer pour de futures améliorations, notamment l'ajout de nouvelles capacités d'outils et de logiques d'agent plus complexes.
