class Numerical():
    def __init__(self):
        self._consent = None
        self._self_soothe1 = None
        self._other_soothe1 = None
        self._self_soothe2 = None
        self._other_soothe2 = None
        self._communication_score = None
        self._communal_strength = None
        self._anxiety = None
    
    def _calc_score(self):
        self._communication_score = self._consent + self._self_soothe1 + self._self_soothe2 + self._other_soothe1 + self._other_soothe2
    
    def _add_strength(self, strength):
        self._communal_strength = strength
    
    def _add_anxiety(self, anxiety):
        self._anxiety = anxiety