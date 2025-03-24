from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

driver = webdriver.Chrome()
queries = [
    
    "-ny-chapter-1-scope-and-administration",
    "chapter-2-definitions",
    "chapter-3-general-regulations",
    "chapter-4-gas-piping-installations",
    "chapter-5-chimneys-and-vents",
    "chapter-6-specific-appliances",
    "chapter-7-gaseous-hydrogen-systems",
    "chapter-8-referenced-standards",
    "appendix-a-sizing-and-capacities-of-gas-piping",
    "appendix-b-sizing-of-venting-systems-serving-appliances-equipped-with-draft-hoods-category-i-appliances-and-appliances-listed-for-use-with-type-b-vents",
    "appendix-d-recommended-procedure-for-safety-inspection-of-an-existing-appliance-installation",
    # "chapter-12-energy-systems",
    # "chapter-13-combustible-dust-producing-operations",
    # "chapter-14-fire-safety-during-construction-alteration-and-demolition",
    # "chapter-15-flammable-finishes",
    # "chapter-16-fruit-and-crop-ripening",
    # "chapter-17-fumigation-and-insecticidal-fogging",
    # "chapter-18-semiconductor-fabrication-facilities",
    # "chapter-19-lumber-yards-and-wood-waste-materials",
    # "chapter-20-aviation-facilities",
    # "chapter-21-dry-cleaning",
    # "chapter-22-combustible-dust-producing-operations",
    # "chapter-23-motor-fuel-dispensing-facilities-and-repair-garages",
    # "chapter-24-flammable-finishes",
    # "chapter-25-fruit-and-crop-ripening",
    # "chapter-26-fumigation-and-insecticidal-fogging",
    # "chapter-27-semiconductor-fabrication-facilities",
    # "chapter-28-lumber-yards-and-agro-industrial-solid-biomass-and-woodworking-facilities",
    # "chapter-29-manufacture-of-organic-coatings",
    # "chapter-30-industrial-ovens",
    # "chapter-31-tents-temporary-special-event-structures-and-other-membrane-structures",
    # "chapter-32-high-piled-combustible-storage",
    # "chapter-33-fire-safety-during-construction-and-demolition",
    # "chapter-34-tire-rebuilding-and-tire-storage",
    # "chapter-35-welding-and-other-hot-work",
    # "chapter-36-marinas",
    # "chapter-37-combustible-fibers",
    # "chapter-38-higher-education-laboratories",
    # "chapter-39-processing-and-extraction-facilities",
    # "-ny-chapter-40-sugarhouse-alternative-activity-provisions",
    # #"chapter-49-fixed-guideway-transit-and-passenger-rail-systems",
    # "chapter-50-hazardous-materials-general-provisions",
    # "chapter-51-aerosols",
    # "chapter-53-compressed-gases",
    # "chapter-54-corrosive-materials",
    # "chapter-55-cryogenic-fluids",
    # "chapter-56-explosives-and-fireworks",
    # "chapter-57-flammable-and-combustible-liquids",
    # "chapter-58-flammable-gases-and-flammable-cryogenic-fluids",
    # "chapter-59-flammable-solids",
    # "chapter-60-highly-toxic-and-toxic-materials",
    # "chapter-61-liquefied-petroleum-gases",
    # "chapter-62-organic-peroxides",
    # "chapter-63-oxidizers-oxidizing-gases-and-oxidizing-cryogenic-fluids",
    # "chapter-64-pyrophoric-materials",
    # "chapter-65-pyroxylin-cellulose-nitrate-plastics",
    # "chapter-66-unstable-reactive-materials",
    # "chapter-67-water-reactive-solids-and-liquids",
    # "chapter-80-referenced-standards",
    # #"appendix-a-board-of-appeals",
    # "appendix-b-fire-flow-requirements-for-buildings",
    # "appendix-c-fire-hydrant-locations-and-distribution",
    # "appendix-d-fire-apparatus-access-roads",
    # "appendix-e-hazard-categories",
    # "appendix-f-hazard-ranking",
    # "appendix-g-cryogenic-fluids-weight-and-volume-equivalents",
    # "appendix-h-hazardous-materials-management-plan-hmmp-and-hazardous-materials-inventory-statement-hmis-instructions",
    # "appendix-i-fire-protection-systems-noncompliant-conditions",
    # "appendix-j-building-information-sign",
    # #"appendix-k-construction-requirements-forexisting-ambulatory-care-facilities",
    # "appendix-l-requirements-for-fire-fighterair-replenishment-systems",
    # #"appendix-m-high-rise-buildings-retroactive-automatic-sprinkler-requirement",
    # "appendix-n-indoor-trade-shows-and-exhibitions",
    
    

]

# Step 2: Iterate over each query and fetch the HTML
for query in queries:
    url = f"https://codes.iccsafe.org/content/NYSFGC2020P1/{query}"
    driver.get(url)

    elems = driver.find_elements(By.CLASS_NAME,"v-main")
    print(f"{len(elems)} elements found")

    for elem in elems:
        d = elem.get_attribute("outerHTML")
        with open(f"data/{query}.html","w",encoding="utf-8") as f:
            f.write(d)
             
        


    time.sleep(5)
driver.close()