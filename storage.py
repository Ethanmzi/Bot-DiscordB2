# storage.py
# Gestion de la sauvegarde JSON + données globales du bot

import json
import os

from structures import StackHistory, TreeNode

DATA_FILE = "data.json"


class Storage:
    def __init__(self, path=DATA_FILE):
        self.path = path
        self.user_histories = {}   # user_id -> StackHistory
        self.command_counts = {}   # user_id -> int
        self.tree_root = None      # racine de l'arbre
        self.sessions = {}         # user_id -> TreeNode (position dans l'arbre)

    def init_default_tree(self):
        """
        Arbre par défaut : aide à choisir un langage de programmation à apprendre.
        """
        from structures import TreeNode

        # Racine : niveau
        root = TreeNode(
            "root",
            "Salut ! Tu veux apprendre un langage de prog.\n"
            "Tu es plutôt débutant ou déjà à l'aise ? (réponds: debutant / avance)"
        )

        # Débutant
        debutant = TreeNode(
            "debutant",
            "Tu préfères faire quoi au début ? (web / script)"
        )
        debutant_web = TreeNode(
            "debutant_web",
            result="Je te conseille **JavaScript** pour commencer le web 🌐"
        )
        debutant_script = TreeNode(
            "debutant_script",
            result="Je te conseille **Python** pour commencer en douceur 🐍"
        )
        debutant.add_child(debutant_web)
        debutant.add_child(debutant_script)

        # Avancé
        avance = TreeNode(
            "avance",
            "Tu veux te diriger vers quoi ? (mobile / backend / data)"
        )
        avance_mobile = TreeNode(
            "avance_mobile",
            result="Pour le mobile, regarde **Kotlin** (Android) ou **Swift** (iOS) 📱"
        )
        avance_backend = TreeNode(
            "avance_backend",
            result="Pour le backend, **Java** ou **C#** sont de bons choix 💻"
        )
        avance_data = TreeNode(
            "avance_data",
            result="Pour la data, reste sur **Python** avec les libs data 📊"
        )
        avance.add_child(avance_mobile)
        avance.add_child(avance_backend)
        avance.add_child(avance_data)

        root.add_child(debutant)
        root.add_child(avance)

        self.tree_root = root


    def load(self):
        """Charge les données depuis le fichier JSON (si présent)."""
        if not os.path.exists(self.path):
            # init par défaut
            self.init_default_tree()
            return

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            # en cas de problème de lecture, on repart sur un arbre propre
            self.init_default_tree()
            return

        # histo
        for user_id, commands in data.get("user_histories", {}).items():
            stack = StackHistory()
            for cmd in commands:
                stack.push(cmd)
            self.user_histories[user_id] = stack

        # counts
        self.command_counts = data.get("command_counts", {})

        # arbre
        tree_data = data.get("tree")
        if tree_data:
            self.tree_root = TreeNode.from_dict(tree_data)
        else:
            self.init_default_tree()

        # sessions (on ne restaure pas les sessions en cours, on repart de zéro)
        self.sessions = {}

    def save(self):
        """Sauvegarde les données en JSON."""
        data = {
            "user_histories": {uid: history.to_list() for uid, history in self.user_histories.items()},
            "command_counts": self.command_counts,
            "tree": self.tree_root.to_dict() if self.tree_root else None
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_history_for(self, user_id):
        """Retourne la pile d'historique de l'utilisateur, en la créant si besoin."""
        if user_id not in self.user_histories:
            self.user_histories[user_id] = StackHistory()
        return self.user_histories[user_id]

    def inc_command_count(self, user_id):
        self.command_counts[user_id] = self.command_counts.get(user_id, 0) + 1
