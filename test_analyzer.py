"""Test du CodeAnalyzer sur OrgUnitsServiceImpl.java"""
from code_analyzer import CodeAnalyzer

# Code Java de test (OrgUnitsServiceImpl.java)
java_code = """package com.airbus.neo.webapp.service.serviceImpl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.airbus.neo.webapp.dao.OrgUnitsDaoImpl;
import com.airbus.neo.webapp.model.OrgUnitsResponse;
import com.airbus.neo.webapp.service.OrgUnitsService;

@Service
public class OrgUnitsServiceImpl implements OrgUnitsService {

    @Autowired
    private OrgUnitsDaoImpl orgUnitsDaoImpl;

    @Override
    public Map<String, Object> getOrgUnitsLabel(String idUO, String personId, String vsid) {
        Map<String, Object> result = new HashMap<>();
        try {
            String label = orgUnitsDaoImpl.getOrgUnitsLabel(idUO, personId, vsid);
            result.put("label", label);
            result.put("success", true);
        } catch (Exception e) {
            result.put("error", e.getMessage());
            result.put("success", false);
        }
        return result;
    }

    @Override
    public List<OrgUnitsResponse> getOrgUnits(String idUO, String personId, String vsid) {
        return orgUnitsDaoImpl.getOrgUnits(idUO, personId, vsid);
    }

    @Override
    public Map<String, Object> getAllOrgUnits(String personId, String vsid) {
        return orgUnitsDaoImpl.getAllOrgUnits(personId, vsid);
    }
}
"""

# Créer l'analyseur
analyzer = CodeAnalyzer(java_code, "OrgUnitsServiceImpl.java")

# Analyser
print("\n" + "="*70)
print("🧪 TEST DE L'ANALYSEUR AMÉLIORÉ")
print("="*70 + "\n")

analyses = analyzer.analyze_all()

print("\n📊 BUG ANALYSIS:")
print(f"Score: {analyses['bug_analysis']['score']}")
print(f"Bugs détectés: {len(analyses['bug_analysis']['bugs'])}")
for bug in analyses['bug_analysis']['bugs']:
    print(f"  ⚠️  Ligne {bug['line']}: {bug['type']} - {bug['description']}")

print("\n🔒 SECURITY ANALYSIS:")
print(f"Score: {analyses['security_analysis']['score']}")
print(f"Vulnérabilités: {len(analyses['security_analysis']['vulnerabilities'])}")
for vuln in analyses['security_analysis']['vulnerabilities']:
    print(f"  🔴 Ligne {vuln['line']}: {vuln['type']} - {vuln['description']}")

print("\n⚡ PERFORMANCE ANALYSIS:")
print(f"Score: {analyses['performance_analysis']['score']}")
print(f"Problèmes: {len(analyses['performance_analysis']['bottlenecks'])}")
for issue in analyses['performance_analysis']['bottlenecks']:
    print(f"  ⚡ Ligne {issue['line']}: {issue['type']} - {issue['description']}")

print("\n" + "="*70)
print("✅ TEST TERMINÉ")
print("="*70 + "\n")

# Vérifications
print("🎯 RÉSULTATS ATTENDUS:")
print("  ✓ Security: PAS de 'HashMap usage detected' (juste import)")
print("  ✓ Security: HashMap détecté uniquement à la ligne 24 (new HashMap<>)")
print("  ✓ Performance: PAS de 'Nested Loops' (aucune boucle dans le code)")
print("  ✓ Performance: PAS de problème de performance (code simple)")
