clear all
import delimited "panel_gender_full.csv", clear

ppmlhdfe monthly_productivity post_treated if gender_final == "male", absorb(hashed_author cohort_id##month_id) vce(cluster hashed_author)
local b_m = _b[post_treated]
local se_m = _se[post_treated]
di "Male: coef=" `b_m' " se=" `se_m' " clusters=" e(N_clust)

ppmlhdfe monthly_productivity post_treated if gender_final == "female", absorb(hashed_author cohort_id##month_id) vce(cluster hashed_author)
local b_f = _b[post_treated]
local se_f = _se[post_treated]
di "Female: coef=" `b_f' " se=" `se_f' " clusters=" e(N_clust)

ppmlhdfe monthly_productivity post_treated, absorb(hashed_author cohort_id##month_id) vce(cluster hashed_author)
local b_all = _b[post_treated]
local se_all = _se[post_treated]
di "Overall: coef=" `b_all' " se=" `se_all' " clusters=" e(N_clust)

clear
set obs 3
gen group = ""
gen coef = .
gen se = .
replace group = "Overall" in 1
replace coef = `b_all' in 1
replace se = `se_all' in 1
replace group = "Male" in 2
replace coef = `b_m' in 2
replace se = `se_m' in 2
replace group = "Female" in 3
replace coef = `b_f' in 3
replace se = `se_f' in 3
export delimited "gender_coefficients_full.csv", replace
list
