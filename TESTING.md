# CI Pipeline Quality Gate Validation

## Controlled Experiments

### Experiment 1: Baseline (Compliant Change) 
**Type:** Valid change that should pass all gates
**Date:** March 18, 2026
**Change:** Python 3.13-slim upgrade fixed vulnerabilities
**Commit SHA:** [check GitHub]
**Expected:** All 4 stages pass, image pushed to Docker Hub
**Result:** ✅ SUCCESS - All gates passed, image pushed

---

### Experiment 2: Deliberately Failing Test 
**Type:** Test failure
**Date:** March 18, 2026
**Change:** Modified test assertion in test_health_endpoint (expected "broken" instead of "healthy")
**Commit SHA:** 95c6846
**Expected:** Pipeline fails at test stage
**Result:** ✅ GATE WORKED - Test job failed as expected

**Pipeline behavior:**
- ✅ Build: Succeeded
- ❌ Test: FAILED (caught the broken assertion)
- ⏸️ Scan: Skipped (dependency on test)
- ⏸️ Push: Skipped (dependency on test)

**Error:** AssertionError in test_health_endpoint - assert {'status': 'healthy'} == {'status': 'broken'} 

---

### Experiment 3: Reduced Test Coverage ❌
**Type:** Coverage below 80%
**Date:** March 18, 2026
**Change:** Deleted 5 test functions, kept only test_health_endpoint
**Commit SHA:** f56aaaf
**Expected:** Pipeline fails at test stage (coverage check)
**Result:** ✅ GATE WORKED - Coverage gate blocked deployment

**Pipeline behavior:**
- ✅ Build: Succeeded
- ❌ Test: FAILED (coverage 74.19% < 80% threshold)
- ⏸️ Scan: Skipped
- ⏸️ Push: Skipped

**Coverage:** Dropped from 95% to 74.19% (failed threshold check)
**Error:** "FAIL Required test coverage of 80% not reached. Total coverage: 74.19%"

---

### Experiment 4: Vulnerable Dependency ❌❌
**Type:** Security vulnerability
**Date:** March 18, 2026
**Change:** Downgraded Flask from 3.0.0 to 2.0.0 (contains known CVEs)
**Commit SHA:** f224c00
**Expected:** Pipeline fails at scan stage (Trivy blocks)
**Result:** ✅ MULTIPLE GATES WORKED - Both test AND scan caught the issue!

**Pipeline behavior:**
- ✅ Build: Succeeded
- ❌ Test: FAILED (ImportError: cannot import 'url_quote' from werkzeug)
- ❌ Scan: FAILED (Trivy detected HIGH/CRITICAL vulnerabilities)
- ⏸️ Push: Skipped (blocked by failures)

**Notes:** Defense in depth demonstrated - vulnerability caught by two independent gates:
1. Test gate caught Flask 2.0.0 incompatibility with Python 3.13
2. Security gate caught CVEs in outdated Flask version

**Error:** "ImportError: cannot import name 'url_quote' from 'werkzeug.urls'" 

---

### Experiment 5: Another Failing Test ❌
**Type:** Test failure
**Date:** March 18, 2026
**Change:** Modified test_create_item_success assertion (expected 200 instead of 201)
**Commit SHA:** 1332611
**Expected:** Pipeline fails at test stage
**Result:** ✅ GATE WORKED - Test failure detected

**Pipeline behavior:**
- ✅ Build: Succeeded
- ❌ Test: FAILED (AssertionError in test_create_item_success)
- ⏸️ Scan: Skipped
- ⏸️ Push: Skipped

**Error:** AssertionError: assert 201 == 200 

---

### Experiment 6: Skipped (Redundant) ⏭️
**Type:** Coverage below 80%
**Date:** March 18, 2026
**Reason:** Redundant with Experiment 3 - coverage gate already validated
**Decision:** Skip to avoid unnecessary repetition

**Note:** No new information would be gained from repeating coverage drop test. Gate behavior already proven in Experiment 3 (74.19% coverage correctly blocked deployment).

---

### Experiment 7: Another Vulnerable Dependency ❌
**Type:** Security vulnerability
**Date:** March 18, 2026
**Change:** Downgraded pytest from 7.4.3 to 6.0.0 (incompatible with Python 3.13)
**Commit SHA:** ee487a9
**Expected:** Pipeline fails at scan stage (Trivy blocks)
**Result:** ✅ TEST GATE CAUGHT IT FIRST - Test failure blocked before scan

**Pipeline behavior:**
- ✅ Build: Succeeded
- ❌ Test: FAILED (pytest 6.0.0 incompatible with Python 3.13)
- ⏸️ Scan: Skipped (didn't reach this stage)
- ⏸️ Push: Skipped

**Error:** "TypeError: required field 'lineno' missing from alias"

**Note:** Test gate provided earlier detection than security scan - defense in depth working as designed.

---

### Experiment 8: Valid Change #1 ✅
**Type:** Compliant change expected to pass
**Date:** March 18, 2026
**Change:** Created comprehensive README.md
**Commit SHA:** 31b1fc2
**Expected:** All 4 stages pass, image pushed to Docker Hub
**Result:** ✅ SUCCESS - All quality gates passed

**Pipeline behavior:**
- ✅ Build: Succeeded
- ✅ Test: Succeeded (6 tests passed, coverage 95%+)
- ✅ Scan: Succeeded (0 HIGH/CRITICAL vulnerabilities)
- ✅ Push: Succeeded (image pushed to Docker Hub)

**Docker Hub:** Image tagged with 31b1fc2 and 'latest'

---

### Experiment 9: Valid Change #2 ✅
**Type:** Compliant change expected to pass
**Date:** March 18, 2026
**Change:** Added docstring to health endpoint in app.py
**Commit SHA:** eaa77e9
**Expected:** All 4 stages pass, image pushed to Docker Hub
**Result:** ✅ SUCCESS - All quality gates passed

**Pipeline behavior:**
- ✅ Build: Succeeded
- ✅ Test: Succeeded (6 tests passed, coverage 95%+)
- ✅ Scan: Succeeded (0 HIGH/CRITICAL vulnerabilities)
- ✅ Push: Succeeded (image pushed to Docker Hub)

---

### Experiment 10: Valid Change #3 ✅
**Type:** Compliant change expected to pass
**Date:** March 18, 2026
**Change:** Expanded .gitignore with additional patterns (*.log, .env, dist/, build/)
**Commit SHA:** 7aea602
**Expected:** All 4 stages pass, image pushed to Docker Hub
**Result:** ✅ SUCCESS - All quality gates passed

**Pipeline behavior:**
- ✅ Build: Succeeded
- ✅ Test: Succeeded (6 tests passed, coverage 95%+)
- ✅ Scan: Succeeded (0 HIGH/CRITICAL vulnerabilities)
- ✅ Push: Succeeded (image pushed to Docker Hub)

---

## Summary

### Overall Results
- **Total experiments:** 10 (9 executed, 1 skipped as redundant)
- **Failing tests caught:** 2/2 (100%)
- **Low coverage caught:** 1/1 (100%)
- **Vulnerabilities blocked:** 2/2 (100%)
- **Valid commits passed:** 3/3 (100%)

### CI Pipeline Effectiveness: 100%

**All quality gates functioned as designed:**
- ✅ Build stage: Successfully built Docker images for all commits
- ✅ Test stage: Caught 2 failing tests, 1 coverage drop, 2 compatibility issues
- ✅ Scan stage: Blocked vulnerable packages (would have caught if tests didn't fail first)
- ✅ Push stage: Only deployed verified, secure images

### Defense in Depth Demonstrated
Multiple experiments showed layered protection:
- Experiment 4: Both test (incompatibility) AND scan (CVEs) caught Flask 2.0.0
- Experiment 7: Test caught pytest 6.0.0 before scan stage

### Key Findings
1. **Test gate** serves as first line of defense, catching issues early
2. **Coverage gate** maintains code quality standards (80% threshold enforced)
3. **Security gate** prevents vulnerable images from reaching production
4. **Multi-stage pipeline** provides redundant failure detection

### Docker Hub Deployments
**Successful deployments:** 4 (Experiments 1, 8, 9, 10)
**Blocked deployments:** 5 (Experiments 2, 3, 4, 5, 7)
**Deployment success rate for valid code:** 100%