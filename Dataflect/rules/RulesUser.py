import re

STOPWORDS = {
    "um",
    "uma",
    "o",
    "a",
    "de",
    "do",
    "da",
    "quero",
    "preciso",
    "gostaria"
}

class RulesSintaxe():

    def __init__(self):
        self.rules = {}
        self.SentimentRules = {}
        self.Memory = {}
        self.similarity_threshold = 0.6
    def __str__(self):
        return "RulesSintaxe"
    def normalize(self, text):
        text = str(text).lower()
        text = re.sub(r"[^\w\s]", "", text)
        tokens = text.split()
        tokens = [
            t for t in tokens
            if t not in STOPWORDS
        ]
        return set(tokens)

    def similarity(self, tokens1, tokens2):
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        if not union:
            return 0
        return len(intersection) / len(union)

    def MemoryData(self, Memory, Rule):
        normalized = self.normalize(Memory)
        self.Memory[Memory] = {
            "tokens": normalized,
            "rule": Rule
        }

    def GetMemory(self, Memory):
        new_tokens = self.normalize(Memory)
        best_match = None
        best_score = 0

        for old_text, data in self.Memory.items():
            old_tokens = data["tokens"]
            score = self.similarity(
                new_tokens,
                old_tokens
            )

            if score > best_score:
                best_score = score
                best_match = data

        if best_score >= self.similarity_threshold:
            return {
                "status": "memory_match",
                "similarity": best_score,
                "action": best_match["rule"]
            }
        return None

    def NewRule(self, rule: tuple, intent, action):
        palavras = tuple(
            p.strip().lower()
            for p in rule
        )

        self.rules[palavras] = {
            "intent": intent,
            "action": action
        }
    
    def NewRuleSentiment(self,ruleSentiment,action):
        pass

    def ResponseRule(self, text, intent):
        palavras_texto = self.normalize(text)
        index_count = 0

        for palavras_regra, dados in self.rules.items():
            Rule = set(palavras_regra)
            if Rule.issubset(palavras_texto):
                self.MemoryData(
                    str(text),
                    dados["action"]
                )
                return {
                    "intent": dados["intent"],
                    "action": dados["action"]
                }

        memory_result = self.GetMemory(text)
        if memory_result:
            return {
                "intent": intent,
                "action": memory_result["action"],
                "source": "memory",
                "similarity": memory_result["similarity"]
            }

        return None