clear all
import delimited "panel_gender_full.csv", clear

ppmlhdfe monthly_productivity rel_month_p* if gender_final == "male", absorb(hashed_author cohort_id##month_id rel_month) vce(cluster hashed_author)
di "Male clusters: " e(N_clust) "  obs: " e(N)

matrix b = e(b)
matrix V = e(V)
local names : colnames b
tempname mh
postfile `mh' str40 coef double estimate double se using "coefs_male.dta", replace
local k = 1
foreach name of local names {
    post `mh' ("`name'") (b[1, `k']) (sqrt(V[`k', `k']))
    local k = `k' + 1
}
postclose `mh'

ppmlhdfe monthly_productivity rel_month_p* if gender_final == "female", absorb(hashed_author cohort_id##month_id rel_month) vce(cluster hashed_author)
di "Female clusters: " e(N_clust) "  obs: " e(N)

matrix b = e(b)
matrix V = e(V)
local names : colnames b
tempname mh
postfile `mh' str40 coef double estimate double se using "coefs_female.dta", replace
local k = 1
foreach name of local names {
    post `mh' ("`name'") (b[1, `k']) (sqrt(V[`k', `k']))
    local k = `k' + 1
}
postclose `mh'
