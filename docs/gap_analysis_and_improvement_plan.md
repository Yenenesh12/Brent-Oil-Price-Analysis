# Capstone Project: Gap Analysis & Improvement Plan

**Project:** Brent Oil Price Analysis - Bayesian Change Point Detection  
**Student:** Yenenesh  
**Date:** February 15, 2026

---

## Executive Summary

This document provides a comprehensive review of the current project state against the capstone rubric requirements, identifies gaps, and outlines a prioritized improvement plan to ensure a "Pass" rating.

**Current Status:** 85% Complete  
**Critical Gaps:** 2 items (Technical Report file, Enhanced Testing)  
**Recommended Timeline:** 8-12 hours total work

---

## 1. Project Selection & Gap Analysis

### 1.1 Review of Past Work

**Strengths Identified:**
- ✅ Solid Bayesian modeling foundation with PyMC implementation
- ✅ Interactive dashboards (both React/Flask and Streamlit)
- ✅ Good data preprocessing and event correlation logic
- ✅ CI/CD pipeline with GitHub Actions configured
- ✅ Type hints and dataclasses implemented across core modules

**Feedback from Previous Iterations:**
- Need more comprehensive testing coverage
- Documentation should include a standalone technical report/blog post
- SHAP visualizations need to be more prominent
- Presentation needs to be finance-audience focused

### 1.2 Current State Assessment

| Rubric Requirement | Status | Evidence | Gap |
|-------------------|--------|----------|-----|
| **Engineering Excellence** |
| Refactored, modular code | ✅ COMPLETE | Type hints in all src/ files, dataclasses used | None |
| Type hints & dataclasses | ✅ COMPLETE | `@dataclass` in data_loader.py, changepoint_model.py | None |
| 5+ unit tests | ⚠️ PARTIAL | 6 tests exist, but need more coverage | Need 2-3 more tests |
| CI/CD with badge | ✅ COMPLETE | .github/workflows/ci.yml + badge in README | None |
| Interactive dashboard | ✅ COMPLETE | Streamlit + React/Flask dashboards | None |
| SHAP visualizations | ✅ COMPLETE | Implemented in predictive_model.py | None |
| **Documentation** |
| Comprehensive README | ✅ COMPLETE | Detailed README with setup, structure, results | None |
| Technical report/blog | ❌ MISSING | Content exists in README but not as standalone file | **CRITICAL GAP** |
| Presentation outline | ⚠️ PARTIAL | Basic outline exists, needs expansion | Need detailed slides |
| **Project Planning** |
| Gap analysis | ❌ MISSING | This document addresses it | Creating now |
| Prioritized tasks | ❌ MISSING | This document addresses it | Creating now |

---

## 2. Identified Gaps (Prioritized)

### 🔴 CRITICAL (Must Fix for Pass)

**Gap 1: Standalone Technical Report/Blog Post**
- **Issue:** Technical report content is embedded in README, not a separate professional document
- **Impact:** Rubric explicitly requires "blog post or technical report"
- **Risk:** High - Could result in automatic fail

**Gap 2: Insufficient Test Coverage**
- **Issue:** Only 6 tests; need more comprehensive coverage of edge cases
- **Impact:** Rubric requires "robust testing (at least 5 unit tests)" - technically met but marginal
- **Risk:** Medium - Need to demonstrate robustness

### 🟡 IMPORTANT (Strongly Recommended)

**Gap 3: Presentation Needs Expansion**
- **Issue:** Outline is too brief; needs actual slide content or detailed speaker notes
- **Impact:** Rubric requires presentation that "effectively communicates business impact"
- **Risk:** Medium - Current outline may not demonstrate effectiveness

**Gap 4: Missing Test for Event Correlator**
- **Issue:** No tests for src/event_correlator.py module
- **Impact:** Incomplete test coverage of core functionality
- **Risk:** Low-Medium - Shows incomplete engineering rigor

### 🟢 NICE TO HAVE (Enhancement)

**Gap 5: Documentation Could Include More Visuals**
- **Issue:** Technical report could benefit from embedded charts/diagrams
- **Impact:** Improves professional presentation quality
- **Risk:** Low - Not explicitly required

---

## 3. Prioritized Improvement Tasks

### Task 1: Create Standalone Technical Report ⏱️ 2 hours
**Priority:** 🔴 CRITICAL  
**Effort:** Medium  
**Justification:** Rubric explicitly requires "blog post or technical report" as separate deliverable

**Action Items:**
1. Extract technical report content from README
2. Create `docs/technical_report.md` with proper formatting
3. Add 2-3 embedded visualizations (charts from outputs/figures/)
4. Ensure 800-1000 word count with professional tone
5. Include proper citations and data sources
6. Add executive summary and conclusion sections

**Success Criteria:**
- Standalone markdown file in docs/
- Finance-audience appropriate language
- Includes business impact metrics
- References visualizations from project

---

### Task 2: Expand Test Suite to 10+ Tests ⏱️ 3 hours
**Priority:** 🔴 CRITICAL  
**Effort:** Medium-High  
**Justification:** Demonstrates robust engineering; current 6 tests are minimal

**Action Items:**
1. Add 3 tests for `src/event_correlator.py`:
   - Test event proximity calculation
   - Test event scoring logic
   - Test edge case (no events in range)
2. Add 2 tests for `src/time_series_analysis.py`:
   - Test stationarity detection
   - Test volatility calculation
3. Add 2 tests for `src/predictive_model.py`:
   - Test VAR model fitting
   - Test SHAP explanation generation
4. Add edge case tests for existing modules:
   - Empty data handling
   - Invalid date ranges
5. Update CI/CD to show test coverage percentage

**Success Criteria:**
- Minimum 10 passing tests
- All core modules have test coverage
- Tests include edge cases and error handling
- CI pipeline passes with all tests

---

### Task 3: Develop Detailed Presentation ⏱️ 2-3 hours
**Priority:** 🟡 IMPORTANT  
**Effort:** Medium  
**Justification:** Rubric requires presentation that "effectively communicates business impact to finance audience"

**Action Items:**
1. Expand `docs/presentation_outline.md` to include:
   - Detailed speaker notes for each slide (2-3 sentences minimum)
   - Specific data points and metrics to highlight
   - Visual descriptions (which charts to show)
2. Create slide deck (PowerPoint/Google Slides) with:
   - 10-12 slides total
   - Title, Problem, Solution, Demo, Results, Impact, Q&A structure
   - Screenshots from dashboard
   - Key metrics prominently displayed
3. Add "What to Say" notes for finance audience:
   - Avoid technical jargon
   - Focus on ROI and risk reduction
   - Use business analogies

**Success Criteria:**
- Detailed presentation outline with speaker notes
- Optional: Actual slide deck (PDF or PPTX)
- Finance-focused language throughout
- Clear business value proposition

---

### Task 4: Add Event Correlator Tests ⏱️ 1 hour
**Priority:** 🟡 IMPORTANT  
**Effort:** Low  
**Justification:** Completes test coverage of all core modules

**Action Items:**
1. Create `tests/test_event_correlator.py`
2. Implement 3 tests:
   - Test correlation scoring
   - Test event filtering by date range
   - Test handling of missing event data
3. Ensure tests pass in CI pipeline

**Success Criteria:**
- New test file with 3+ passing tests
- Event correlator module fully tested
- CI pipeline remains green

---

### Task 5: Enhance Documentation with Visuals ⏱️ 1-2 hours
**Priority:** 🟢 NICE TO HAVE  
**Effort:** Low-Medium  
**Justification:** Improves professional quality and readability

**Action Items:**
1. Add architecture diagram to README
2. Embed 2-3 key charts in technical report
3. Add flowchart of analysis workflow
4. Include screenshot of dashboard in README

**Success Criteria:**
- At least 3 visual elements in documentation
- Images properly referenced and displayed
- Professional appearance

---

## 4. Implementation Timeline

### Phase 1: Critical Fixes (Days 1-2) - 5 hours
- ✅ Task 1: Create technical report (2 hours)
- ✅ Task 2: Expand test suite (3 hours)

### Phase 2: Important Enhancements (Day 3) - 3 hours
- ✅ Task 3: Develop presentation (2-3 hours)
- ✅ Task 4: Event correlator tests (1 hour)

### Phase 3: Polish (Day 4) - 2 hours
- ✅ Task 5: Documentation visuals (1-2 hours)
- ✅ Final review and validation

**Total Estimated Time:** 8-12 hours

---

## 5. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Technical report not accepted as separate deliverable | Low | High | Create as standalone .md file with clear structure |
| Test suite still deemed insufficient | Medium | High | Aim for 10+ tests with edge cases |
| Presentation not finance-focused enough | Low | Medium | Use business metrics, avoid jargon |
| CI/CD pipeline breaks with new tests | Low | Medium | Test locally before committing |
| Time overrun on tasks | Medium | Low | Prioritize Tasks 1-2, defer Task 5 if needed |

---

## 6. Success Metrics

**Project will achieve "Pass" rating when:**
- ✅ Standalone technical report exists in `docs/technical_report.md` (800+ words)
- ✅ Test suite has 10+ passing tests covering all core modules
- ✅ CI/CD pipeline passes with green badge
- ✅ Presentation outline includes detailed speaker notes
- ✅ All code uses type hints and dataclasses
- ✅ Interactive dashboard is functional
- ✅ SHAP visualizations are generated and documented
- ✅ README is comprehensive with setup instructions

---

## 7. Validation Checklist

Before final submission, verify:

**Engineering Excellence:**
- [ ] All Python files in src/ use type hints
- [ ] Dataclasses used for data structures
- [ ] 10+ unit tests passing
- [ ] CI/CD pipeline green with badge in README
- [ ] Dashboard runs without errors
- [ ] SHAP visualizations generated

**Documentation:**
- [ ] README has setup, structure, results sections
- [ ] Standalone technical report in docs/ (800+ words)
- [ ] Presentation outline with speaker notes
- [ ] All documentation uses finance-appropriate language

**Project Planning:**
- [ ] This gap analysis document exists
- [ ] Tasks are prioritized with time estimates
- [ ] Justifications provided for each task

---

## 8. Conclusion

The project is in strong shape with 85% completion. The two critical gaps (standalone technical report and expanded testing) can be addressed in 5 hours of focused work. Completing all five tasks will ensure a confident "Pass" rating with professional-quality deliverables.

**Recommended Action:** Execute Tasks 1-2 immediately (critical), then Tasks 3-4 (important), and Task 5 if time permits.

**Next Steps:**
1. Create `docs/technical_report.md` (Task 1)
2. Expand test suite to 10+ tests (Task 2)
3. Enhance presentation with speaker notes (Task 3)
4. Add event correlator tests (Task 4)
5. Polish documentation with visuals (Task 5)

---

**Document Version:** 1.0  
**Last Updated:** February 15, 2026  
**Status:** Ready for Implementation
