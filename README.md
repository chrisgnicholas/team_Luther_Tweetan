This is Luther_Tweetan's team repository.

We examine the potential of uniformly introducing fortified beans and millet into the Ugandan diet, coming from the 'HarvestPlus' program:
https://www.harvestplus.org/
and examine an alternative, extremely targeted "nutrient pack" intervention costing ~$1 US/week/child, in terms of its potential to reduce the 'Disability Adjusted Life Years' (DALYs) of Ugandan children.

If we’d had more time, we would have explored adding a nutrition pack as a new FCT item, with an expense of $0.15 USD, run the minimal adequate diet calculations of Project2, and looked at the differences. That would have given use some basis to explore public outreach, focused on avoidable DALYs in children, to shift overall household's utility function to favor the nutrition packs.

Our nutrient pack is based upon the 20g "Lipid-based Nutrient Supplement (LNS-SQ) paste" package of:
https://supply.unicef.org/s0000323.html

Our cost of $1/week and effectiveness is based upon:
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10564609/

and the documentation provided in the misc/SQ-LNS.pdf document, as well as the Global Burden of Disease Visualization tools:
https://vizhub.healthdata.org/gbd-results/


Files:
    Code_final.ipynb: 
	final Jupyter notebook

    pop_profiles.ipynb: 
	a separate notebook with population profile graphs

    get_subsidy_increase.py: 
	support code to calculate per-household subsidies, given a policy
	of counting children under 9 years of age. 

    utils.py:
	support routines for notebooks

	misc/ 
		various documents of the Ugandan national nutritional situation and strategy, and technical information about the effectiveness of SQ-LNS interventions on children.
	
