import os
import shutil
import fitz  # PyMuPDF library  # type: ignore
from datetime import datetime
from PIL import Image, ImageTk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

# Marketing Sources Mapping
MARKETING_SOURCES = [
    "SEM (youtube/search words/google)",
    "Digital (autotrader/weather network/OBJ)",
    "SEO (google my business)",
    "Social media (facebook/Instagram/linkedin)",
    "Website fees",
    "Radio/TV",
    "Print materials (magazines/newspaper)",
    "Promo materials (bags/business cards)",
    "Out of Home (OOH) -this includes billboards/mailouts",
    "Video/photograph",
    "Sponsorships",
    "Events (test drive event)",
    "Influencers",
    "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)",
    "Operations/facility- (signage/COVID)",
    "Communications – mailchimp/mobile ap",
    "DAG Group fees",
    "VAUTO/CARFAX"
]

# Matrix mapping Account and Source to GL Code for Audi locations
AUDI_MATRIX = {
    "Split All Division": {
        "SEM (youtube/search words/google)": "M/H6014A",
        "Digital (autotrader/weather network/OBJ)": "M/H6014B",
        "SEO (google my business)": "M/H6014C",
        "Social media (facebook/Instagram/linkedin)": "M/H6014D",
        "Website fees": "M/H6014E",
        "Radio/TV": "M/H6014F",
        "Print materials (magazines/newspaper)": "M/H6014G",
        "Promo materials (bags/business cards)": "M/H6015H",
        "Out of Home (OOH) -this includes billboards/mailouts": "M/H6014I",
        "Video/photograph": "M/H6014J",
        "Sponsorships": "M/H6015K",
        "Events (test drive event)": "M/H6015L",
        "Influencers": "M/H6015M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "M/H6014N",
        "Operations/facility- (signage/COVID)": "M/H6014O",
        "Communications – mailchimp/mobile ap": "M/H6014P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": "M/H/L 6259"
    },
    "New Car (1)": {
        "SEM (youtube/search words/google)": "M/H6114A",
        "Digital (autotrader/weather network/OBJ)": "M/H6114B",
        "SEO (google my business)": "M/H6114C",
        "Social media (facebook/Instagram/linkedin)": "M/H6114D",
        "Website fees": "M/H6114E",
        "Radio/TV": "M/H6114F",
        "Print materials (magazines/newspaper)": "M/H6114G",
        "Promo materials (bags/business cards)": "M/H6115H",
        "Out of Home (OOH) -this includes billboards/mailouts": "M/H6114I",
        "Video/photograph": "M/H6114J",
        "Sponsorships": "M/H6115K",
        "Events (test drive event)": "M/H6115L",
        "Influencers": "M/H6115M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "M/H6114N",
        "Operations/facility- (signage/COVID)": "M/H6114O",
        "Communications – mailchimp/mobile ap": "M/H6114P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": "M/H/L 6259"
    },
    "Used car (2)": {
        "SEM (youtube/search words/google)": "M/H6214A",
        "Digital (autotrader/weather network/OBJ)": "M/H6214B",
        "SEO (google my business)": "M/H6214C",
        "Social media (facebook/Instagram/linkedin)": "M/H6214D",
        "Website fees": "M/H6214E",
        "Radio/TV": "M/H6214F",
        "Print materials (magazines/newspaper)": "M/H6214G",
        "Promo materials (bags/business cards)": "M/H6215H",
        "Out of Home (OOH) -this includes billboards/mailouts": "M/H6214I",
        "Video/photograph": "M/H6214J",
        "Sponsorships": "M/H6215K",
        "Events (test drive event)": "M/H6215L",
        "Influencers": "M/H6215M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "M/H6214N",
        "Operations/facility- (signage/COVID)": "M/H6214O",
        "Communications – mailchimp/mobile ap": "M/H6214P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": "M/H/L 6259"
    },
    "Service (4)": {
        "SEM (youtube/search words/google)": "M/H6414A",
        "Digital (autotrader/weather network/OBJ)": "M/H6414B",
        "SEO (google my business)": "M/H6414C",
        "Social media (facebook/Instagram/linkedin)": "M/H6414D",
        "Website fees": "M/H6414E",
        "Radio/TV": "M/H6414F",
        "Print materials (magazines/newspaper)": "M/H6414G",
        "Promo materials (bags/business cards)": "M/H6415H",
        "Out of Home (OOH) -this includes billboards/mailouts": "M/H6414I",
        "Video/photograph": "M/H6414J",
        "Sponsorships": "M/H6415K",
        "Events (test drive event)": "M/H6415L",
        "Influencers": "M/H6415M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "M/H6414N",
        "Operations/facility- (signage/COVID)": "M/H6414O",
        "Communications – mailchimp/mobile ap": "M/H6414P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": "M/H/L 6259"
    },
    "body shop (5)": {
        "SEM (youtube/search words/google)": "M6514A",
        "Digital (autotrader/weather network/OBJ)": "M6514B",
        "SEO (google my business)": "M6514C",
        "Social media (facebook/Instagram/linkedin)": "M6514D",
        "Website fees": "M6514E",
        "Radio/TV": "M6514F",
        "Print materials (magazines/newspaper)": "M6514G",
        "Promo materials (bags/business cards)": "M6515H",
        "Out of Home (OOH) -this includes billboards/mailouts": "M6514I",
        "Video/photograph": "M6514J",
        "Sponsorships": "M6515K",
        "Events (test drive event)": "M6515L",
        "Influencers": "M6515M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "M6514N",
        "Operations/facility- (signage/COVID)": "M6514O",
        "Communications – mailchimp/mobile ap": "M6514P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": "M/H/L 6259"
    },
    "Parts (7)": {
        "SEM (youtube/search words/google)": "M/H6754A",
        "Digital (autotrader/weather network/OBJ)": "M/H6714B",
        "SEO (google my business)": "M/H6714C",
        "Social media (facebook/Instagram/linkedin)": "M/H6714D",
        "Website fees": "M/H6714E",
        "Radio/TV": "M/H6714F",
        "Print materials (magazines/newspaper)": "M/H6714G",
        "Promo materials (bags/business cards)": "M/H6715H",
        "Out of Home (OOH) -this includes billboards/mailouts": "M/H6714I",
        "Video/photograph": "M/H6714J",
        "Sponsorships": "M/H6715K",
        "Events (test drive event)": "M/H6715L",
        "Influencers": "M/H6715M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "M/H6714N",
        "Operations/facility- (signage/COVID)": "M/H6714O",
        "Communications – mailchimp/mobile ap": "M/H6714P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": "M/H/L 6259"
    }
}

# Matrix mapping Account and Source to GL Code for Jaguar
JAGUAR_MATRIX = {
    "Split Jag and LR (All Division)": {
        "SEM (youtube/search words/google)": "905000A",
        "Digital (autotrader/weather network/OBJ)": "905000B",
        "SEO (google my business)": "905000C",
        "Social media (facebook/Instagram/linkedin)": "905000D",
        "Website fees": "905100E",
        "Radio/TV": "905000F",
        "Print materials (magazines/newspaper)": "905000G",
        "Promo materials (bags/business cards)": "904000H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905000I",
        "Video/photograph": "905000J",
        "Sponsorships": "904000K",
        "Events (test drive event)": "904000L",
        "Influencers": "904000M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905000N",
        "Operations/facility- (signage/COVID)": "905000O",
        "Communications – mailchimp/mobile ap": "905000P",
        "DAG Group fees": "905100Q",
        "VAUTO/CARFAX": "JLR 6259"
    },
    "New Jag (Jaguar New Car)": {
        "SEM (youtube/search words/google)": "905010A",
        "Digital (autotrader/weather network/OBJ)": "905010B",
        "SEO (google my business)": "905010C",
        "Social media (facebook/Instagram/linkedin)": "905010D",
        "Website fees": "905110E",
        "Radio/TV": "905010F",
        "Print materials (magazines/newspaper)": "905010G",
        "Promo materials (bags/business cards)": "904010H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905010I",
        "Video/photograph": "905010J",
        "Sponsorships": "904010K",
        "Events (test drive event)": "904010L",
        "Influencers": "904010M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905010N",
        "Operations/facility- (signage/COVID)": "905010O",
        "Communications – mailchimp/mobile ap": "905010P",
        "DAG Group fees": "905110Q",
        "VAUTO/CARFAX": "JLR 6259"
    },
    "PO Jag (Jaguar Used Car)": {
        "SEM (youtube/search words/google)": "905012A",
        "Digital (autotrader/weather network/OBJ)": "905012B",
        "SEO (google my business)": "905012C",
        "Social media (facebook/Instagram/linkedin)": "905012D",
        "Website fees": "905112E",
        "Radio/TV": "905012F",
        "Print materials (magazines/newspaper)": "905012G",
        "Promo materials (bags/business cards)": "904012H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905012I",
        "Video/photograph": "905012J",
        "Sponsorships": "904012K",
        "Events (test drive event)": "904012L",
        "Influencers": "904012M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905012N",
        "Operations/facility- (signage/COVID)": "905012O",
        "Communications – mailchimp/mobile ap": "905012P",
        "DAG Group fees": "905112Q",
        "VAUTO/CARFAX": "JLR 6259"
    },
    "Srv Jag (Jaguar Service)": {
        "SEM (youtube/search words/google)": "905013A",
        "Digital (autotrader/weather network/OBJ)": "905013B",
        "SEO (google my business)": "905013C",
        "Social media (facebook/Instagram/linkedin)": "905013D",
        "Website fees": "905113E",
        "Radio/TV": "905013F",
        "Print materials (magazines/newspaper)": "905013G",
        "Promo materials (bags/business cards)": "904013H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905013I",
        "Video/photograph": "905013J",
        "Sponsorships": "904013K",
        "Events (test drive event)": "904013L",
        "Influencers": "904013M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905013N",
        "Operations/facility- (signage/COVID)": "905013O",
        "Communications – mailchimp/mobile ap": "905013P",
        "DAG Group fees": "905113Q",
        "VAUTO/CARFAX": "JLR 6259"
    },
    "Parts Jag (Jaguar Parts)": {
        "SEM (youtube/search words/google)": "905014A",
        "Digital (autotrader/weather network/OBJ)": "905014B",
        "SEO (google my business)": "905014C",
        "Social media (facebook/Instagram/linkedin)": "905014D",
        "Website fees": "905114E",
        "Radio/TV": "905014F",
        "Print materials (magazines/newspaper)": "905014G",
        "Promo materials (bags/business cards)": "904014H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905014I",
        "Video/photograph": "905014J",
        "Sponsorships": "904014K",
        "Events (test drive event)": "904014L",
        "Influencers": "904014M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905014N",
        "Operations/facility- (signage/COVID)": "905014O",
        "Communications – mailchimp/mobile ap": "905014P",
        "DAG Group fees": "905114Q",
        "VAUTO/CARFAX": "JLR 6259"
    }
}

# Matrix mapping Account and Source to GL Code for Landrover
LANDROVER_MATRIX = {
    "Split Jag and LR (All Division)": {
        "SEM (youtube/search words/google)": "905000A",
        "Digital (autotrader/weather network/OBJ)": "905000B",
        "SEO (google my business)": "905000C",
        "Social media (facebook/Instagram/linkedin)": "905000D",
        "Website fees": "905100E",
        "Radio/TV": "905000F",
        "Print materials (magazines/newspaper)": "905000G",
        "Promo materials (bags/business cards)": "904000H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905000I",
        "Video/photograph": "905000J",
        "Sponsorships": "904000K",
        "Events (test drive event)": "904000L",
        "Influencers": "904000M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905000N",
        "Operations/facility- (signage/COVID)": "905000O",
        "Communications – mailchimp/mobile ap": "905000P",
        "DAG Group fees": "905100Q",
        "VAUTO/CARFAX": "JLR 6259"
    },
    "New LR (Landrover New Car)": {
        "SEM (youtube/search words/google)": "905020A",
        "Digital (autotrader/weather network/OBJ)": "905020B",
        "SEO (google my business)": "905020C",
        "Social media (facebook/Instagram/linkedin)": "905020D",
        "Website fees": "905120E",
        "Radio/TV": "905020F",
        "Print materials (magazines/newspaper)": "905020G",
        "Promo materials (bags/business cards)": "904020H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905020I",
        "Video/photograph": "905020J",
        "Sponsorships": "904020K",
        "Events (test drive event)": "904020L",
        "Influencers": "904020M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905020N",
        "Operations/facility- (signage/COVID)": "905020O",
        "Communications – mailchimp/mobile ap": "905020P",
        "DAG Group fees": "905120Q",
        "VAUTO/CARFAX": "JLR 6259"
    },
    "PO LR (Landrover Used Car)": {
        "SEM (youtube/search words/google)": "905022A",
        "Digital (autotrader/weather network/OBJ)": "905022B",
        "SEO (google my business)": "905022C",
        "Social media (facebook/Instagram/linkedin)": "905022D",
        "Website fees": "905122E",
        "Radio/TV": "905022F",
        "Print materials (magazines/newspaper)": "905022G",
        "Promo materials (bags/business cards)": "904022H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905022I",
        "Video/photograph": "905022J",
        "Sponsorships": "904022K",
        "Events (test drive event)": "904022L",
        "Influencers": "904022M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905022N",
        "Operations/facility- (signage/COVID)": "905022O",
        "Communications – mailchimp/mobile ap": "905022P",
        "DAG Group fees": "905122Q",
        "VAUTO/CARFAX": "JLR 6259"
    },
    "Srv LR (Landrover Service)": {
        "SEM (youtube/search words/google)": "905023A",
        "Digital (autotrader/weather network/OBJ)": "905023B",
        "SEO (google my business)": "905023C",
        "Social media (facebook/Instagram/linkedin)": "905023D",
        "Website fees": "905123E",
        "Radio/TV": "905023F",
        "Print materials (magazines/newspaper)": "905023G",
        "Promo materials (bags/business cards)": "904023H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905023I",
        "Video/photograph": "905023J",
        "Sponsorships": "904023K",
        "Events (test drive event)": "904023L",
        "Influencers": "904023M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905023N",
        "Operations/facility- (signage/COVID)": "905023O",
        "Communications – mailchimp/mobile ap": "905023P",
        "DAG Group fees": "905123Q",
        "VAUTO/CARFAX": "JLR 6259"
    },
    "Parts LR (Landrover Parts)": {
        "SEM (youtube/search words/google)": "905024A",
        "Digital (autotrader/weather network/OBJ)": "905024B",
        "SEO (google my business)": "905024C",
        "Social media (facebook/Instagram/linkedin)": "905024D",
        "Website fees": "905124E",
        "Radio/TV": "905024F",
        "Print materials (magazines/newspaper)": "905024G",
        "Promo materials (bags/business cards)": "904024H",
        "Out of Home (OOH) -this includes billboards/mailouts": "905024I",
        "Video/photograph": "905024J",
        "Sponsorships": "904024K",
        "Events (test drive event)": "904024L",
        "Influencers": "904024M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "905024N",
        "Operations/facility- (signage/COVID)": "905024O",
        "Communications – mailchimp/mobile ap": "905024P",
        "DAG Group fees": "905124Q",
        "VAUTO/CARFAX": "JLR 6259"
    }
}

# Base matrix mapping for Alfa Romeo Maserati (A/Z prefix logic handled at runtime)
ALFA_MAS_MATRIX = {
    "New Car": {
        "SEM (youtube/search words/google)": "3180A",
        "Digital (autotrader/weather network/OBJ)": "3180B",
        "SEO (google my business)": "3180C",
        "Social media (facebook/Instagram/linkedin)": "3180D",
        "Website fees": "3180E",
        "Radio/TV": "3090F",
        "Print materials (magazines/newspaper)": "3090G",
        "Promo materials (bags/business cards)": "3090H",
        "Out of Home (OOH) -this includes billboards/mailouts": "3090I",
        "Video/photograph": "3090J",
        "Sponsorships": "3090K",
        "Events (test drive event)": "3090L",
        "Influencers": "3090M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "3180N",
        "Operations/facility- (signage/COVID)": "3090O",
        "Communications – mailchimp/mobile ap": "3180P",
        "DAG Group fees": "3180Q",
        "VAUTO/CARFAX": "NA"
    },
    "Used car": {
        "SEM (youtube/search words/google)": "3380A",
        "Digital (autotrader/weather network/OBJ)": "3380B",
        "SEO (google my business)": "3380C",
        "Social media (facebook/Instagram/linkedin)": "3380D",
        "Website fees": "3380E",
        "Radio/TV": "3290F",
        "Print materials (magazines/newspaper)": "3290G",
        "Promo materials (bags/business cards)": "3290H",
        "Out of Home (OOH) -this includes billboards/mailouts": "3290I",
        "Video/photograph": "3290J",
        "Sponsorships": "3290K",
        "Events (test drive event)": "3290L",
        "Influencers": "3290M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "3380N",
        "Operations/facility- (signage/COVID)": "3290O",
        "Communications – mailchimp/mobile ap": "3380P",
        "DAG Group fees": "3380Q",
        "VAUTO/CARFAX": "6259"
    },
    "Service": {
        "SEM (youtube/search words/google)": "NA",
        "Digital (autotrader/weather network/OBJ)": "NA",
        "SEO (google my business)": "NA",
        "Social media (facebook/Instagram/linkedin)": "NA",
        "Website fees": "NA",
        "Radio/TV": "3431F",
        "Print materials (magazines/newspaper)": "3431G",
        "Promo materials (bags/business cards)": "3431H",
        "Out of Home (OOH) -this includes billboards/mailouts": "3431I",
        "Video/photograph": "3431J",
        "Sponsorships": "3431K",
        "Events (test drive event)": "3431L",
        "Influencers": "3431M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "NA",
        "Operations/facility- (signage/COVID)": "3431M",
        "Communications – mailchimp/mobile ap": "NA",
        "DAG Group fees": "NA",
        "VAUTO/CARFAX": "NA"
    },
    "Parts": {
        "SEM (youtube/search words/google)": "NA",
        "Digital (autotrader/weather network/OBJ)": "NA",
        "SEO (google my business)": "NA",
        "Social media (facebook/Instagram/linkedin)": "NA",
        "Website fees": "NA",
        "Radio/TV": "3530F",
        "Print materials (magazines/newspaper)": "3530G",
        "Promo materials (bags/business cards)": "3530H",
        "Out of Home (OOH) -this includes billboards/mailouts": "3530I",
        "Video/photograph": "3530J",
        "Sponsorships": "3530K",
        "Events (test drive event)": "3530L",
        "Influencers": "3530M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "NA",
        "Operations/facility- (signage/COVID)": "3530M",
        "Communications – mailchimp/mobile ap": "NA",
        "DAG Group fees": "NA",
        "VAUTO/CARFAX": "NA"
    }
}

CORNWALL_VW_MATRIX = {
    "Split All Division": {
        "SEM (youtube/search words/google)": "6014A",
        "Digital (autotrader/weather network/OBJ)": "6014B",
        "SEO (google my business)": "6014C",
        "Social media (facebook/Instagram/linkedin)": "6014D",
        "Website fees": "6013E",
        "Radio/TV": "6014F",
        "Print materials (magazines/newspaper)": "6014G",
        "Promo materials (bags/business cards)": "6015H",
        "Out of Home (OOH) -this includes billboards/mailouts": "6014I",
        "Video/photograph": "6014J",
        "Sponsorships": "6015K",
        "Events (test drive event)": "6015L",
        "Influencers": "6015M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "6014N",
        "Operations/facility- (signage/COVID)": "6014O",
        "Communications – mailchimp/mobile ap": "6014P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": ""
    },
    "New Car (1)": {
        "SEM (youtube/search words/google)": "6114A",
        "Digital (autotrader/weather network/OBJ)": "6114B",
        "SEO (google my business)": "6114C",
        "Social media (facebook/Instagram/linkedin)": "6114D",
        "Website fees": "6113E",
        "Radio/TV": "6114F",
        "Print materials (magazines/newspaper)": "6114G",
        "Promo materials (bags/business cards)": "6115H",
        "Out of Home (OOH) -this includes billboards/mailouts": "6114I",
        "Video/photograph": "6114J",
        "Sponsorships": "6115K",
        "Events (test drive event)": "6115L",
        "Influencers": "6115M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "6114N",
        "Operations/facility- (signage/COVID)": "6114O",
        "Communications – mailchimp/mobile ap": "6114P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": ""
    },
    "Used car (2)": {
        "SEM (youtube/search words/google)": "6214A",
        "Digital (autotrader/weather network/OBJ)": "6214B",
        "SEO (google my business)": "6214B",
        "Social media (facebook/Instagram/linkedin)": "6214D",
        "Website fees": "6213E",
        "Radio/TV": "6214H",
        "Print materials (magazines/newspaper)": "6214G",
        "Promo materials (bags/business cards)": "6215H",
        "Out of Home (OOH) -this includes billboards/mailouts": "6214I",
        "Video/photograph": "6214J",
        "Sponsorships": "6215K",
        "Events (test drive event)": "6215L",
        "Influencers": "6215M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "6214N",
        "Operations/facility- (signage/COVID)": "6214O",
        "Communications – mailchimp/mobile ap": "6214P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": ""
    },
    "Service (4)": {
        "SEM (youtube/search words/google)": "6414A",
        "Digital (autotrader/weather network/OBJ)": "6414B",
        "SEO (google my business)": "6414C",
        "Social media (facebook/Instagram/linkedin)": "6414D",
        "Website fees": "6413E",
        "Radio/TV": "6414F",
        "Print materials (magazines/newspaper)": "6414G",
        "Promo materials (bags/business cards)": "6415H",
        "Out of Home (OOH) -this includes billboards/mailouts": "6414I",
        "Video/photograph": "6414J",
        "Sponsorships": "6415K",
        "Events (test drive event)": "6415L",
        "Influencers": "6415M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "6414N",
        "Operations/facility- (signage/COVID)": "6414O",
        "Communications – mailchimp/mobile ap": "6414P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": ""
    },
    "Parts (7)": {
        "SEM (youtube/search words/google)": "6714A",
        "Digital (autotrader/weather network/OBJ)": "6714B",
        "SEO (google my business)": "6714C",
        "Social media (facebook/Instagram/linkedin)": "6714D",
        "Website fees": "6713E",
        "Radio/TV": "6714F",
        "Print materials (magazines/newspaper)": "6714G",
        "Promo materials (bags/business cards)": "6715H",
        "Out of Home (OOH) -this includes billboards/mailouts": "6714I",
        "Video/photograph": "6714J",
        "Sponsorships": "6715K",
        "Events (test drive event)": "6715L",
        "Influencers": "6715M",
        "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)": "6714N",
        "Operations/facility- (signage/COVID)": "6714O",
        "Communications – mailchimp/mobile ap": "6714P",
        "DAG Group fees": "",
        "VAUTO/CARFAX": ""
    }
}

class MonthSelector(tb.Toplevel):
    def __init__(self, parent, base_path):
        super().__init__(parent)
        self.title("Select Month")
        self.geometry("420x360")
        self.parent = parent
        self.base_path = base_path
        self.result = None
        
        self.setup_ui()
        self.center_on_screen()

    def setup_ui(self):
        container = tb.Frame(self, padding=25)
        container.pack(fill="both", expand=True)
        
        tb.Label(container, text="Select Invoice Month", font=("Helvetica", 15, "bold"), bootstyle="primary").pack(pady=(0, 15))
        
        # Standard 12 month folder names
        standard_months = [
            "01_January", "02_February", "03_March", "04_April",
            "05_May", "06_June", "07_July", "08_August",
            "09_September", "10_October", "11_November", "12_December"
        ]
        
        # Get existing month folders from network drive if available
        existing_months = []
        if os.path.exists(self.base_path):
            try:
                existing_months = [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]
                existing_months.sort(key=lambda x: os.path.getmtime(os.path.join(self.base_path, x)), reverse=True)
            except Exception:
                existing_months = []
                
        # Combine: existing months first, then any standard months not yet created
        all_months = list(existing_months)
        for sm in standard_months:
            if sm not in all_months:
                all_months.append(sm)
            
        self.month_var = tb.StringVar()
        self.month_btn = tb.Menubutton(container, textvariable=self.month_var, bootstyle="outline-primary")
        self.month_btn.pack(fill="x", pady=10)
        
        self.month_menu = tb.Menu(self.month_btn, tearoff=0)
        for m in all_months:
            self.month_menu.add_command(label=m, command=lambda val=m: self.month_var.set(val))
        self.month_btn['menu'] = self.month_menu
        
        # Default selection: current month matching format or first available
        current_m_num = datetime.now().strftime("%m")
        current_m_name = datetime.now().strftime("%B")
        current_standard = f"{current_m_num}_{current_m_name}"
        
        if current_standard in all_months:
            self.month_var.set(current_standard)
        elif all_months:
            self.month_var.set(all_months[0])
            
        btn_frame = tb.Frame(container)
        btn_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        tb.Button(btn_frame, text="Cancel", command=self.destroy, bootstyle="outline-secondary").pack(side="left", expand=True, fill="x", padx=(0, 5))
        tb.Button(btn_frame, text="Open", command=self.on_open, bootstyle="primary").pack(side="right", expand=True, fill="x", padx=(5, 0))

    def on_open(self):
        selected = self.month_var.get().strip()
        if selected:
            path = os.path.join(self.base_path, selected)
            pending = os.path.join(path, "Pending")
            locations = os.path.join(path, "Locations")
            original = os.path.join(path, "Original")
            
            # Auto-create month folder and top-level folders if they don't exist
            for folder in [path, pending, locations, original]:
                if not os.path.exists(folder):
                    os.makedirs(folder)
            
            # Auto-create all 12 dealership folders inside Locations
            dealerships = [
                "Alfa-Mas",
                "Audi City Ottawa",
                "Audi Ottawa",
                "Audi West Ottawa",
                "Cornwall Centre Volkswagen",
                "INEOS",
                "JLR",
                "Mercedes-Benz",
                "MMG",
                "Porsche",
                "Split",
                "Volkswagen de l'Outaouais"
            ]
            for dealer in dealerships:
                dealer_path = os.path.join(locations, dealer)
                if not os.path.exists(dealer_path):
                    os.makedirs(dealer_path)
                
            self.result = (pending, locations, original)
            self.destroy()

    def center_on_screen(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

class InvoiceStamperApp:
    def __init__(self, root, input_dir, output_dir, archive_dir):
        self.root = root
        self.root.title("Mark Motors Group - Invoice Automation")
        self.root.geometry("1400x900")
        
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.archive_dir = archive_dir
        
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(input_dir):
            messagebox.showerror("Error", f"Input directory '{input_dir}' does not exist.")
            self.pdf_files = []
        else:
            self.pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        
        self.current_index = 0
        self.current_pdf_doc = None  
        self.last_location = ""
        # UI Elements (initialized here to help IDE/Linter)
        self.preview_container = None
        self.preview_label = None
        self.right_frame = None
        self.scroll_frame = None
        self.scroll_content = None
        self.scrollbar = None
        self.title_label = None
        self.status_label = None
        self.loc_combo = None
        self.split_container = None
        self.gl_entry = None
        self.desc_entry = None
        self.date_entry = None
        self.process_btn = None
        self.nav_frame = None
        self.back_btn = None
        self.skip_btn = None
        self.finish_btn = None
        self.add_btn = None
        self.balance_btn = None
        self.split_placeholder = None
        self.btn_frame = None
        self.main_container = None
        self.split_container = None
        self.split_rows_frame = None
        self.split_controls = None
        self.split_header = None
        self.scroll_id = None
        self.scroll_content = None
        self.loc_entry = None
        self.loc_var = None
        self.acc_btn = None
        self.acc_var = None
        self.source_btn = None
        self.source_var = None
        self.charge_var = None
        self.charge_entry = None
        self.split_rows = [] # List of dicts: {"frame": Frame, "loc": StringVar, "perc": StringVar}
        self.preview_images = [] # Keep references to PhotoImage objects
        
        self.drag_start_x = None
        self.drag_start_y = None
        self.active_canvas = None
        self.drag_rect_id = None
        
        self.setup_ui()
        self.load_current_pdf()

    def get_locations(self):
        order = [
            "Alfa-Mas",
            "Audi City Ottawa",
            "Audi Ottawa",
            "Audi West Ottawa",
            "Cornwall Centre Volkswagen",
            "INEOS",
            "JLR",
            "Mercedes-Benz",
            "MMG",
            "Porsche",
            "Split",
            "Volkswagen de l'Outaouais"
        ]
        try:
            dirs = [d for d in os.listdir(self.output_dir) if os.path.isdir(os.path.join(self.output_dir, d))]
            locations = [d for d in dirs if d.lower() not in ["__pycache__", ".git"]]
            
            result = []
            for item in order:
                match = next((d for d in locations if d.lower() == item.lower()), None)
                if match:
                    result.append(match)
            for d in locations:
                if d.lower() not in [x.lower() for x in order]:
                    result.append(d)
            return result
        except Exception:
            return order

    def update_account_options(self, location):
        if location == "Select Location..." or not location:
            return
            
        self.acc_menu.delete(0, "end")
        loc_lower = location.lower()
        
        if any(x in loc_lower for x in ["audi", "city ottawa"]):
            options = [
                "Split All Division",
                "New Car (1)",
                "Used car (2)",
                "Service (4)",
                "body shop (5)",
                "Parts (7)"
            ]
        elif "cornwall" in loc_lower:
            options = [
                "Split All Division",
                "New Car (1)",
                "Used car (2)",
                "Service (4)",
                "Parts (7)"
            ]
        elif "jlr" in loc_lower:
            options = [
                "Split Jag and LR (All Division)",
                "New Jag (Jaguar New Car)",
                "PO Jag (Jaguar Used Car)",
                "Srv Jag (Jaguar Service)",
                "Parts Jag (Jaguar Parts)",
                "New LR (Landrover New Car)",
                "PO LR (Landrover Used Car)",
                "Srv LR (Landrover Service)",
                "Parts LR (Landrover Parts)"
            ]
        elif "alfa" in loc_lower or "maserati" in loc_lower:
            options = [
                "Alfa - New Car",
                "Alfa - Used Car",
                "Alfa - Service",
                "Alfa - Parts",
                "Maserati - New Car",
                "Maserati - Used Car",
                "Maserati - Service",
                "Maserati - Parts"
            ]
        else:
            options = [
                "Split All Division",
                "New Car",
                "Used Car",
                "Service",
                "Body Shop",
                "Parts"
            ]
            
        for opt in options:
            self.acc_menu.add_command(label=opt, command=lambda val=opt: self.on_acc_select(val))
            
        self.acc_var.set("Select Account...")

    def on_acc_select(self, selection):
        self.acc_var.set(selection)
        self.update_expense_details()

    def get_gl_code(self, location, account, source):
        if not source or source == "Select Source...":
            return ""
            
        loc_lower = location.lower()
        
        # 1. Audi Locations
        if any(x in loc_lower for x in ["audi", "city ottawa"]):
            audi_key = account
            if account == "New Car": audi_key = "New Car (1)"
            elif account == "Used Car": audi_key = "Used car (2)"
            elif account == "Service": audi_key = "Service (4)"
            elif account == "Body Shop": audi_key = "body shop (5)"
            elif account == "Parts": audi_key = "Parts (7)"
            elif account == "Split All": audi_key = "Split All Division"
            
            if audi_key in AUDI_MATRIX:
                return AUDI_MATRIX[audi_key].get(source, "")
            return ""
            
        # 1b. Cornwall Location
        elif "cornwall" in loc_lower:
            cw_key = account
            if account == "New Car": cw_key = "New Car (1)"
            elif account == "Used Car": cw_key = "Used car (2)"
            elif account == "Service": cw_key = "Service (4)"
            elif account == "Parts": cw_key = "Parts (7)"
            elif account == "Split All": cw_key = "Split All Division"
            
            if cw_key in CORNWALL_VW_MATRIX:
                return CORNWALL_VW_MATRIX[cw_key].get(source, "")
            return ""
            
        # 2. JLR Location
        elif "jlr" in loc_lower:
            if "LR" in account or "Landrover" in account:
                lr_key = account
                if "New LR" in account: lr_key = "New LR (Landrover New Car)"
                elif "PO LR" in account: lr_key = "PO LR (Landrover Used Car)"
                elif "Srv LR" in account: lr_key = "Srv LR (Landrover Service)"
                elif "Parts LR" in account: lr_key = "Parts LR (Landrover Parts)"
                elif "Split" in account: lr_key = "Split Jag and LR (All Division)"
                
                if lr_key in LANDROVER_MATRIX:
                     return LANDROVER_MATRIX[lr_key].get(source, "")
            else:
                jag_key = account
                if "New Jag" in account: jag_key = "New Jag (Jaguar New Car)"
                elif "PO Jag" in account: jag_key = "PO Jag (Jaguar Used Car)"
                elif "Srv Jag" in account: jag_key = "Srv Jag (Jaguar Service)"
                elif "Parts Jag" in account: jag_key = "Parts Jag (Jaguar Parts)"
                elif "Split" in account: jag_key = "Split Jag and LR (All Division)"
                
                if jag_key in JAGUAR_MATRIX:
                     return JAGUAR_MATRIX[jag_key].get(source, "")
            return ""
            
        # 3. Alfa Romeo Maserati Location
        elif "alfa" in loc_lower or "maserati" in loc_lower:
            brand = "Alfa"
            if "maserati" in account.lower() or "mas" in account.lower():
                brand = "Maserati"
            
            base_col = "New Car"
            if "used" in account.lower(): base_col = "Used car"
            elif "service" in account.lower(): base_col = "Service"
            elif "parts" in account.lower(): base_col = "Parts"
            
            if base_col in ALFA_MAS_MATRIX:
                code_suffix = ALFA_MAS_MATRIX[base_col].get(source, "")
                if code_suffix == "NA" or not code_suffix:
                    return code_suffix
                prefix = "A" if brand == "Alfa" else "Z"
                return prefix + code_suffix
            return ""
            
        return ""

    def setup_ui(self):
        # Header with Logo
        header_frame = tb.Frame(self.root, bootstyle="dark", padding=10)
        header_frame.pack(fill="x")
        
        try:
            logo_img = Image.open("logo.png")
            # Maintain aspect ratio
            logo_img.thumbnail((250, 60), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo_img)
            logo_label = tb.Label(header_frame, image=self.logo_tk, bootstyle="dark")
            logo_label.pack(side="left", padx=20)
        except Exception:
            tb.Label(header_frame, text="MARK MOTORS GROUP", font=("Helvetica", 20, "bold"), bootstyle="inverse-dark").pack(side="left", padx=20)
            
        tb.Label(header_frame, text="INVOICE AUTOMATION", font=("Outfit", 16, "bold"), bootstyle="inverse-dark").pack(side="right", padx=30)

        # Bottom Status Bar
        self.status_bar = tb.Frame(self.root, bootstyle="secondary", padding=5)
        self.status_bar.pack(side="bottom", fill="x")
        
        self.status_bar_label = tb.Label(self.status_bar, text="Ready", font=("Helvetica", 10), bootstyle="inverse-secondary")
        self.status_bar_label.pack(side="left", padx=10)

        # Main Layout
        self.main_container = tb.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        self.main_container.columnconfigure(0, weight=3) # Left (PDF)
        self.main_container.columnconfigure(1, weight=1) # Right (Form)
        self.main_container.rowconfigure(0, weight=1)

        # --- Left Frame: PDF Preview ---
        self.left_frame = tb.Frame(self.main_container, padding=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Scrollable Canvas for multi-page preview
        self.preview_canvas = tb.Canvas(self.left_frame, highlightthickness=0)
        self.preview_scrollbar = tb.Scrollbar(self.left_frame, orient="vertical", command=self.preview_canvas.yview)
        self.preview_canvas.configure(yscrollcommand=self.preview_scrollbar.set)
        
        self.preview_scrollbar.pack(side="right", fill="y")
        self.preview_canvas.pack(side="left", fill="both", expand=True)
        
        self.preview_content = tb.Frame(self.preview_canvas, bootstyle="secondary")
        self.preview_window = self.preview_canvas.create_window((0, 0), window=self.preview_content, anchor="nw")
        
        # Sync width and scrollregion
        self.preview_canvas.bind("<Configure>", self._on_preview_canvas_configure)
        self.preview_content.bind("<Configure>", lambda e: self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all")))

        # Global mousewheel binding
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- Right Frame: Form Inputs ---
        self.right_frame = tb.Frame(self.main_container, padding=20)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Scrollable area for form if many split rows
        self.scroll_frame = tb.Canvas(self.right_frame)
        self.scroll_content = tb.Frame(self.scroll_frame)
        self.scrollbar = tb.Scrollbar(self.right_frame, orient="vertical", command=self.scroll_frame.yview)
        self.scroll_frame.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_frame.pack(side="left", fill="both", expand=True)
        self.scroll_id = self.scroll_frame.create_window((0, 0), window=self.scroll_content, anchor="nw")
        
        # Ensure scroll content fits the canvas width
        self.scroll_frame.bind("<Configure>", self._on_canvas_configure)
        self.scroll_content.bind("<Configure>", lambda e: self.scroll_frame.configure(scrollregion=self.scroll_frame.bbox("all")))

        # Title Card
        title_container = tb.Frame(self.right_frame)
        title_container.pack(fill="x", pady=(0, 20), anchor="w")
        
        self.title_label = tb.Label(title_container, text="Invoice Information", font=("Outfit", 20, "bold"), bootstyle="primary")
        self.title_label.pack(anchor="w")
        
        self.status_label = tb.Label(title_container, text="Loading...", font=("Helvetica", 11), bootstyle="secondary")
        self.status_label.pack(anchor="w")

        tb.Separator(self.right_frame).pack(fill="x", pady=(0, 20))

        # Input fields
        tb.Label(self.scroll_content, text="Location:", font=("Helvetica", 12)).pack(anchor="w")
        self.loc_var = tb.StringVar()
        self.loc_var.set("Select Location...")
        
        self.loc_btn = tb.Menubutton(self.scroll_content, textvariable=self.loc_var, bootstyle="outline-primary")
        self.loc_btn.pack(fill="x", pady=(0, 10))
        
        self.loc_menu = tb.Menu(self.loc_btn, tearoff=0)
        self.loc_btn['menu'] = self.loc_menu
        for opt in self.get_locations():
            self.loc_menu.add_command(label=opt, command=lambda val=opt: self.on_loc_select(val))

        tb.Label(self.scroll_content, text="Account:", font=("Helvetica", 12)).pack(anchor="w")
        self.acc_var = tb.StringVar()
        self.acc_var.set("Select Account...")
        
        self.acc_btn = tb.Menubutton(self.scroll_content, textvariable=self.acc_var, bootstyle="outline-primary")
        self.acc_btn.pack(fill="x", pady=(0, 10))
        
        self.acc_menu = tb.Menu(self.acc_btn, tearoff=0)
        self.acc_btn['menu'] = self.acc_menu
        for opt in ["Select Location First..."]:
            self.acc_menu.add_command(label=opt, command=lambda val=opt: self.on_acc_select(val))

        tb.Label(self.scroll_content, text="Source:", font=("Helvetica", 12)).pack(anchor="w")
        self.source_var = tb.StringVar()
        self.source_var.set("Select Source...")
        
        self.source_btn = tb.Menubutton(self.scroll_content, textvariable=self.source_var, bootstyle="outline-primary")
        self.source_btn.pack(fill="x", pady=(0, 10))
        
        self.source_menu = tb.Menu(self.source_btn, tearoff=0)
        self.source_btn['menu'] = self.source_menu
        for opt in MARKETING_SOURCES:
            self.source_menu.add_command(label=opt, command=lambda val=opt: self.on_source_select(val))

        # --- Dynamic Split Container ---
        self.split_container = tb.Labelframe(self.scroll_content, text="Split Distribution", padding=15, bootstyle="info")
        # We don't pack it yet; shown only for Split/Split All
        
        self.split_header = tb.Frame(self.split_container)
        self.split_header.pack(fill="x", pady=(0, 5))
        tb.Label(self.split_header, text="Location", font=("Helvetica", 10, "bold"), bootstyle="secondary").pack(side="left", expand=True, fill="x")
        tb.Label(self.split_header, text="%", font=("Helvetica", 10, "bold"), bootstyle="secondary", width=6).pack(side="left", padx=(5, 45))

        self.split_rows_frame = tb.Frame(self.split_container)
        self.split_rows_frame.pack(fill="x")

        # Total Percentage Bar
        self.total_frame = tb.Frame(self.split_container)
        self.total_frame.pack(fill="x", pady=(10, 0))
        
        self.total_label = tb.Label(self.total_frame, text="Current Total: 0.0%", font=("Helvetica", 10, "bold"))
        self.total_label.pack(side="right")

        self.split_controls = tb.Frame(self.split_container)
        self.split_controls.pack(fill="x", pady=(15, 0))
        
        self.add_btn = tb.Button(self.split_controls, text="+ Add Row", command=self.add_split_row, bootstyle="outline-info", width=12)
        self.add_btn.pack(side="left")
        
        self.balance_btn = tb.Button(self.split_controls, text="Balance Remaining", command=self.balance_percentages, bootstyle="link-info")
        self.balance_btn.pack(side="right")

        # Regular Fields
        tb.Label(self.scroll_content, text="GL Code", font=("Helvetica", 10, "bold"), bootstyle="secondary").pack(anchor="w", pady=(20, 0))
        self.gl_var = tb.StringVar()
        self.gl_entry = tb.Entry(self.scroll_content, textvariable=self.gl_var, font=("Helvetica", 12))
        self.gl_entry.pack(fill="x", pady=(5, 15))
        
        # We bind KeyRelease so typing updates it live, but FocusOut ensures it updates if pasted
        self.gl_entry.bind("<KeyRelease>", self.on_gl_change)
        self.gl_entry.bind("<FocusOut>", self.on_gl_change)

        tb.Label(self.scroll_content, text="Description", font=("Helvetica", 10, "bold"), bootstyle="secondary").pack(anchor="w")
        self.desc_var = tb.StringVar()
        self.desc_entry = tb.Entry(self.scroll_content, textvariable=self.desc_var, font=("Helvetica", 12))
        self.desc_entry.pack(fill="x", pady=(5, 15))

        tb.Label(self.scroll_content, text="Date", font=("Helvetica", 10, "bold"), bootstyle="secondary").pack(anchor="w")
        self.date_var = tb.StringVar()
        self.date_entry = tb.Entry(self.scroll_content, textvariable=self.date_var, font=("Helvetica", 12))
        self.date_entry.pack(fill="x", pady=(5, 15))

        tb.Label(self.scroll_content, text="Charge Description (Filename)", font=("Helvetica", 10, "bold"), bootstyle="secondary").pack(anchor="w")
        self.charge_var = tb.StringVar()
        self.charge_entry = tb.Entry(self.scroll_content, textvariable=self.charge_var, font=("Helvetica", 12))
        self.charge_entry.pack(fill="x", pady=(5, 30))

        tb.Separator(self.scroll_content).pack(fill="x", pady=20)

        # --- Action Buttons ---
        
        # Process Button (Big Green)
        self.process_btn = tb.Button(
            self.scroll_content, text="✓ Process & Next", 
            command=self.process_pdf, bootstyle="success", width=25
        )
        self.process_btn.pack(fill="x", pady=(0, 10), ipady=12)

        # Skip and Go Back in a row
        self.nav_frame = tb.Frame(self.scroll_content)
        self.nav_frame.pack(fill="x", pady=(0, 10))
        
        self.back_btn = tb.Button(
            self.nav_frame, text="⇠ Go Back", 
            command=self.go_back, bootstyle="outline-secondary"
        )
        self.back_btn.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=8)

        self.skip_btn = tb.Button(
            self.nav_frame, text="Skip ⇢", 
            command=self.skip_pdf, bootstyle="outline-secondary"
        )
        self.skip_btn.pack(side="right", expand=True, fill="x", padx=(5, 0), ipady=8)

        # Finish Button
        self.finish_btn = tb.Button(
            self.scroll_content, text="✕ Finish & Close", 
            command=self.root.destroy, bootstyle="outline-danger", width=25
        )
        self.finish_btn.pack(fill="x", pady=(20, 0), ipady=12)
        
    def _on_canvas_configure(self, event):
        # Update width of scrollable frame to match canvas
        self.scroll_frame.itemconfig(self.scroll_id, width=event.width)
    def _on_preview_canvas_configure(self, event):
        # Update width of PDF preview content to match canvas
        self.preview_canvas.itemconfig(self.preview_window, width=event.width)

    def _on_mousewheel(self, event):
        # Determine which canvas to scroll based on mouse position
        widget = self.root.winfo_containing(event.x_root, event.y_root)
        if not widget: return
        
        # Check if we are over the PDF preview or its children
        is_preview = False
        curr = widget
        while curr:
            if curr == self.preview_canvas:
                is_preview = True
                break
            curr = curr.master
            
        # Check if we are over the form scroll area
        is_form = False
        if not is_preview:
            curr = widget
            while curr:
                if curr == self.scroll_frame:
                    is_form = True
                    break
                curr = curr.master

        if is_preview:
            self.preview_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif is_form:
            self.scroll_frame.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def on_loc_select(self, selection):
        self.loc_var.set(selection)
        if selection == "Split":
            self.split_container.pack(fill="x", after=self.source_btn)
            if not self.split_rows:
                self.add_split_row()
        else:
            self.split_container.pack_forget()
            self.clear_splits()
        self.update_account_options(selection)
        self.update_expense_details()

    def on_source_select(self, selection):
        self.source_var.set(selection)
        if selection and selection != "Select Source...":
            # Auto-suggest charge description for the filename (user can customize/rename freely)
            short_source = selection.split("(")[0].strip()
            self.charge_var.set(short_source)
        self.update_expense_details()

    def get_description_for_source_and_loc(self, source, loc):
        if source == "VAUTO/CARFAX":
            return "USED CAR DEPT."
            
        loc_lower = loc.lower()
        is_audi = any(x in loc_lower for x in ["audi", "city ottawa"])
        is_jlr = "jlr" in loc_lower
        is_alfa = "alfa" in loc_lower or "maserati" in loc_lower
        is_cornwall = "cornwall" in loc_lower
        
        if is_audi:
            if source in ["Promo materials (bags/business cards)", "Sponsorships", "Events (test drive event)", "Influencers"]:
                return "Sales Promotion"
            return "Advertising"
        elif is_cornwall:
            if source in ["Promo materials (bags/business cards)", "Sponsorships", "Events (test drive event)", "Influencers"]:
                return "Sales Promotion"
            elif source == "Website fees":
                return "Advertising fees"
            return "Advertising"
        elif is_jlr:
            if source in ["Website fees", "DAG Group fees"]:
                return "AD group"
            return "Advertising"
        elif is_alfa:
            if source in ["SEM (youtube/search words/google)", "Digital (autotrader/weather network/OBJ)", 
                          "SEO (google my business)", "Social media (facebook/Instagram/linkedin)", 
                          "Website fees", "Software solutions/reputation management/chat (Mobials/Rapid Response/live persons)", 
                          "Communications – mailchimp/mobile ap", "DAG Group fees"]:
                return "Internet only"
            return "Print/media"
        else:
            if source in ["Promo materials (bags/business cards)", "Sponsorships", "Events (test drive event)", "Influencers"]:
                return "Sales Promotion"
            return "Advertising"

    def update_expense_details(self, *args):
        loc = self.loc_var.get().strip()
        acc = self.acc_var.get().strip()
        source = self.source_var.get().strip()
        
        # If no source is selected, we cannot determine GL code or description
        if not source or source == "Select Source...":
            return
            
        # Determine description based on source and location
        desc = self.get_description_for_source_and_loc(source, loc)
        self.desc_var.set(desc)
        
        # Determine GL Code
        gl_code = ""
        if loc == "Split":
            # For split, we compile a combined GL Code from the split rows
            gl_codes = []
            for row in self.split_rows:
                l = row["loc"].get()
                if l and l != "Select...":
                    code = self.get_gl_code(l, acc, source)
                    if code and code != "NA" and code not in gl_codes:
                        gl_codes.append(code)
            if gl_codes:
                gl_code = " / ".join(gl_codes)
        else:
            gl_code = self.get_gl_code(loc, acc, source)
            
        if gl_code:
            self.gl_var.set(gl_code)

    def add_split_row(self, location="", percentage=""):
        row_frame = tb.Frame(self.split_rows_frame)
        row_frame.pack(fill="x", pady=5)
        
        loc_var = tb.StringVar(value=location or "Select...")
        loc_btn = tb.Menubutton(row_frame, textvariable=loc_var, bootstyle="outline-secondary", width=15)
        loc_btn.pack(side="left", expand=True, fill="x")
        
        split_menu = tb.Menu(loc_btn, tearoff=0)
        for split_loc in [l for l in self.get_locations() if l != "Split"]:
            split_menu.add_command(label=split_loc, command=lambda v=split_loc, var=loc_var: var.set(v))
        loc_btn['menu'] = split_menu
        
        perc_var = tb.StringVar(value=percentage)
        perc_entry = tb.Entry(row_frame, textvariable=perc_var, width=8, font=("Helvetica", 11), justify="center")
        perc_entry.pack(side="left", padx=5)
        
        # Add a '%' label
        tb.Label(row_frame, text="%", font=("Helvetica", 10), bootstyle="secondary").pack(side="left", padx=(0, 5))
        
        del_btn = tb.Button(row_frame, text="✕", bootstyle="danger-outline", width=3,
                           command=lambda f=row_frame: self.remove_split_row(f))
        del_btn.pack(side="left")
        
        # Track for live total and updates
        perc_var.trace_add("write", lambda *args: self.update_total_percentage())
        loc_var.trace_add("write", lambda *args: self.update_expense_details())
        
        self.split_rows.append({"frame": row_frame, "loc": loc_var, "perc": perc_var})
        self.update_total_percentage()

    def remove_split_row(self, frame):
        for i, row in enumerate(self.split_rows):
            if row["frame"] == frame:
                row["frame"].destroy()
                self.split_rows.pop(i)
                break
        self.update_total_percentage()

    def update_total_percentage(self):
        total = 0.0
        for row in self.split_rows:
            try:
                val = float(row["perc"].get() or 0)
                total += val
            except ValueError:
                pass
        
        self.total_label.config(text=f"Current Total: {total:.1f}%")
        
        # Highlight based on status
        if abs(total - 100.0) < 0.01:
            self.total_label.config(bootstyle="success")
            self.split_container.config(bootstyle="success")
        elif total > 100.0:
            self.total_label.config(bootstyle="danger")
            self.split_container.config(bootstyle="danger")
        else:
            self.total_label.config(bootstyle="warning")
            self.split_container.config(bootstyle="info")

    def clear_splits(self):
        for row in self.split_rows:
            row["frame"].destroy()
        self.split_rows = []

    def balance_percentages(self):
        if not self.split_rows: return
        
        total = 0.0
        target_row = None
        
        for row in self.split_rows:
            val = row["perc"].get().strip()
            if val:
                try: total += float(val)
                except ValueError: pass
            else:
                target_row = row
        
        if not target_row:
            target_row = self.split_rows[-1]
            try: total -= float(target_row["perc"].get())
            except ValueError: pass
            
        remainder = max(0.0, 100.0 - total)
        target_row["perc"].set(f"{remainder:.1f}")

    def sync_fields_from_gl(self):
        code = self.gl_var.get().strip().upper()
        if not code:
            return
            
        if getattr(self, '_syncing_gl', False):
            return
            
        self._syncing_gl = True
        try:
            matrices = [
                ("Audi Ottawa", AUDI_MATRIX),
                ("JLR", JAGUAR_MATRIX),
                ("Alfa-Mas", ALFA_MAS_MATRIX),
                ("Cornwall Centre Volkswagen", CORNWALL_VW_MATRIX)
            ]
            
            available_locations = self.get_locations()
            
            def find_loc(kw):
                for l in available_locations:
                    if kw.lower() in l.lower():
                        return l
                return None
                
            found = False
            for loc_name, matrix in matrices:
                for acc_name, sources in matrix.items():
                    for src_name, gl in sources.items():
                        if matrix == ALFA_MAS_MATRIX:
                            if code == "A" + gl or code == "Z" + gl or (gl == "6259" and (code == "A6259" or code == "Z6259")):
                                brand_loc = find_loc("Alfa") if code.startswith("A") else find_loc("Maserati")
                                if not brand_loc:
                                    brand_loc = find_loc("Alfa-Mas")
                                actual_loc = brand_loc
                                actual_acc = "Alfa - " + acc_name if code.startswith("A") else "Maserati - " + acc_name
                                self.loc_var.set(actual_loc)
                                self.update_account_options(actual_loc)
                                self.acc_var.set(actual_acc)
                                self.source_var.set(src_name)
                                found = True
                                break
                        elif gl == code:
                            actual_loc = find_loc("Audi") if "AUDI" in loc_name.upper() else find_loc("Cornwall") if "CORNWALL" in loc_name.upper() else find_loc("JLR")
                            if not actual_loc:
                                actual_loc = loc_name
                                
                            if "JLR" in actual_loc.upper() or "JAG" in actual_loc.upper() or "LAND" in actual_loc.upper():
                                if any(code.startswith(x) for x in ["90502", "90402", "90512"]):
                                    actual_acc = "New LR (Landrover New Car)" if "New LR" in acc_name else \
                                                 "PO LR (Landrover Used Car)" if "PO LR" in acc_name else \
                                                 "Srv LR (Landrover Service)" if "Srv LR" in acc_name else \
                                                 "Parts LR (Landrover Parts)" if "Parts LR" in acc_name else \
                                                 "Split Jag and LR (All Division)"
                                else:
                                    actual_acc = "New Jag (Jaguar New Car)" if "New Jag" in acc_name else \
                                                 "PO Jag (Jaguar Used Car)" if "PO Jag" in acc_name else \
                                                 "Srv Jag (Jaguar Service)" if "Srv Jag" in acc_name else \
                                                 "Parts Jag (Jaguar Parts)" if "Parts Jag" in acc_name else \
                                                 "Split Jag and LR (All Division)"
                            else:
                                actual_acc = acc_name
                                
                            self.loc_var.set(actual_loc)
                            self.update_account_options(actual_loc)
                            self.acc_var.set(actual_acc)
                            self.source_var.set(src_name)
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
        finally:
            self._syncing_gl = False

    def on_gl_change(self, event):
        # Auto fill the description based on the mapping smoothly
        code = self.gl_var.get().strip()
        
        # Try to sync dropdowns from the typed GL code
        self.sync_fields_from_gl()
        
        # Update description based on current GL code
        code_upper = code.upper()
        if "6259" in code_upper:
            self.desc_var.set("USED CAR DEPT.")
        elif "15" in code_upper or "090" in code_upper or "290" in code_upper or "4000" in code_upper or "4010" in code_upper or "4020" in code_upper:
            self.desc_var.set("Sales Promotion")
        elif "13" in code_upper or "113" in code_upper or "100" in code_upper or "110" in code_upper or "120" in code_upper:
            self.desc_var.set("Advertising fees" if "CORNWALL" in self.loc_var.get().upper() else "AD group" if "JLR" in self.loc_var.get().upper() else "Internet only" if any(x in self.loc_var.get().lower() for x in ["alfa", "maserati"]) else "Advertising")
        elif "14" in code_upper or "180" in code_upper or "380" in code_upper or "5000" in code_upper or "5010" in code_upper or "5012" in code_upper or "5013" in code_upper or "5014" in code_upper or "5020" in code_upper or "5022" in code_upper or "5023" in code_upper or "5024" in code_upper:
            self.desc_var.set("Internet only" if any(x in self.loc_var.get().lower() for x in ["alfa", "maserati"]) and any(x in code_upper for x in ["3180", "3380"]) else "Print/media" if any(x in self.loc_var.get().lower() for x in ["alfa", "maserati"]) else "Advertising")
        elif "431" in code_upper:
            self.desc_var.set("Print/media" if any(x in self.loc_var.get().lower() for x in ["alfa", "maserati"]) else "Advertising")
        elif "530" in code_upper:
            self.desc_var.set("Print/media" if any(x in self.loc_var.get().lower() for x in ["alfa", "maserati"]) else "Advertising")

    def sanitize_filename(self, text):
        """Remove invalid characters for filenames."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '')
        # Also remove potential newlines or other non-printable characters
        return "".join(c for c in text if c.isprintable()).strip()

    def load_current_pdf(self):
        # Update Back button state
        if self.current_index > 0:
            self.back_btn.config(state="normal")
        else:
            self.back_btn.config(state="disabled")

        # Check if we hit the end
        if self.current_index >= len(self.pdf_files):
            self.status_label.config(text="All Invoices Processed!")
            self.title_label.config(text="Finished Batch")
            
            # Clear previous preview
            for widget in self.preview_content.winfo_children():
                widget.destroy()
            self.preview_images = []
            
            tb.Label(self.preview_content, text="No more PDFs to process.\nClick 'Go Back' or 'Finish & Close'.", 
                     font=("Helvetica", 14), bootstyle="secondary").pack(pady=100)
            
            # Disable inputs & forward flow
            self.process_btn.config(state="disabled")
            self.skip_btn.config(state="disabled")
            self.loc_btn.config(state="disabled")
            self.acc_btn.config(state="disabled")
            self.source_btn.config(state="disabled")
            self.gl_entry.config(state="disabled")
            self.desc_entry.config(state="disabled")
            self.date_entry.config(state="disabled")
            
            # Draw attention to finish/back
            self.finish_btn.configure(bootstyle="danger")
            return
            
        # If we are processing normally, ensure inputs are enabled
        self.process_btn.config(state="normal")
        self.skip_btn.config(state="normal")
        self.loc_btn.config(state="normal")
        self.acc_btn.config(state="normal")
        self.source_btn.config(state="normal")
        self.gl_entry.config(state="normal")
        self.desc_entry.config(state="normal")
        self.date_entry.config(state="normal")

        # Clear previous preview
        for widget in self.preview_content.winfo_children():
            widget.destroy()
        self.preview_images = []
        
        filename = self.pdf_files[self.current_index]
        self.status_label.config(text=f"File {self.current_index + 1} of {len(self.pdf_files)} • {filename}")
        self.title_label.config(text="Invoice Information")
        
        # Reset form but remember Location and set today's Date
        self.loc_var.set(self.last_location)
        if self.last_location and self.last_location != "Select Location...":
            self.update_account_options(self.last_location)
        self.acc_var.set("Select Account...")
        self.source_var.set("Select Source...")
        self.gl_var.set("")
        self.desc_var.set("")
        self.charge_var.set("")
        self.date_var.set(datetime.now().strftime("%m/%d/%Y"))
        
        input_path = os.path.join(self.input_dir, filename)
        try:
            if self.current_pdf_doc:
                self.current_pdf_doc.close()
                
            self.current_pdf_doc = fitz.open(input_path)
            doc = self.current_pdf_doc

            # Dynamically size based on canvas width
            self.preview_canvas.update_idletasks()
            canvas_width = self.preview_canvas.winfo_width()
            target_width = max(600, canvas_width - 30) # Account for scrollbar and padding

            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Render to an image (Pixmap)
                zoom = 1.5 # Balance quality and performance
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                
                # Fit to width
                ratio = target_width / float(img.size[0])
                target_height = int(float(img.size[1]) * ratio)
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                tk_img = ImageTk.PhotoImage(img)
                self.preview_images.append(tk_img) # Keep reference
                
                # Canvas for interactive selection
                page_canvas = tb.Canvas(self.preview_content, width=target_width, height=target_height, highlightthickness=0, cursor="xterm")
                page_canvas.pack(pady=10, padx=10, anchor="center")
                page_canvas.create_image(0, 0, anchor="nw", image=tk_img)
                
                # Bind selection events
                page_canvas.bind("<Button-1>", lambda event, p_num=page_num, t_w=target_width, t_h=target_height: self.on_canvas_press(event, p_num, t_w, t_h))
                page_canvas.bind("<B1-Motion>", self.on_canvas_drag)
                page_canvas.bind("<ButtonRelease-1>", lambda event, p_num=page_num, t_w=target_width, t_h=target_height: self.on_canvas_release(event, p_num, t_w, t_h))
            
            # Scroll to top
            self.preview_canvas.yview_moveto(0)
        except Exception as e:
            tb.Label(self.preview_content, text=f"Could not load preview:\n{e}").pack(pady=20)

        # Put cursor back in GL box (since Location is now a button)
        self.gl_entry.focus()

    def on_canvas_press(self, event, page_num, target_width, target_height):
        # Record start coordinates and widget
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.active_canvas = event.widget
        
        # Clear any existing selection rectangle on this canvas
        if hasattr(self, 'drag_rect_id') and self.drag_rect_id:
            try:
                self.active_canvas.delete(self.drag_rect_id)
            except Exception:
                pass
        
        # Create a dashed selection rectangle
        self.drag_rect_id = self.active_canvas.create_rectangle(
            self.drag_start_x, self.drag_start_y, self.drag_start_x, self.drag_start_y,
            outline="#007fff", width=2, dash=(4, 4)
        )

    def on_canvas_drag(self, event):
        if not hasattr(self, 'drag_rect_id') or not self.drag_rect_id or not hasattr(self, 'active_canvas'):
            return
        # Constrain coordinates to active canvas size
        canvas_width = self.active_canvas.winfo_width()
        canvas_height = self.active_canvas.winfo_height()
        cur_x = max(0, min(event.x, canvas_width))
        cur_y = max(0, min(event.y, canvas_height))
        self.active_canvas.coords(self.drag_rect_id, self.drag_start_x, self.drag_start_y, cur_x, cur_y)

    def on_canvas_release(self, event, page_num, target_width, target_height):
        if not hasattr(self, 'drag_rect_id') or not self.drag_rect_id or not hasattr(self, 'active_canvas'):
            return
        
        end_x = event.x
        end_y = event.y
        
        # Constrain coordinates
        x0 = max(0, min(self.drag_start_x, end_x))
        y0 = max(0, min(self.drag_start_y, end_y))
        x1 = min(target_width, max(self.drag_start_x, end_x))
        y1 = min(target_height, max(self.drag_start_y, end_y))
        
        is_click = (x1 - x0 < 4) and (y1 - y0 < 4)
        
        doc = self.current_pdf_doc
        if not doc or page_num >= len(doc):
            return
        page = doc[page_num]
        
        pdf_w = page.rect.width
        pdf_h = page.rect.height
        
        scale_x = pdf_w / target_width
        scale_y = pdf_h / target_height
        
        copied_text = ""
        
        if is_click:
            # Single click word lookup
            pdf_click_x = x0 * scale_x
            pdf_click_y = y0 * scale_y
            
            words = page.get_text("words") # tuples: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
            margin = 3
            for w in words:
                w_x0, w_y0, w_x1, w_y1, word_text = w[:5]
                if (w_x0 - margin <= pdf_click_x <= w_x1 + margin) and (w_y0 - margin <= pdf_click_y <= w_y1 + margin):
                    copied_text = word_text
                    break
        else:
            # Drag selection
            pdf_x0 = x0 * scale_x
            pdf_y0 = y0 * scale_y
            pdf_x1 = x1 * scale_x
            pdf_y1 = y1 * scale_y
            
            rect = fitz.Rect(pdf_x0, pdf_y0, pdf_x1, pdf_y1)
            copied_text = page.get_text("text", clip=rect).strip()
            
        if copied_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(copied_text)
            self.root.update()
            
            # Change rectangle outline to solid green for confirmation
            self.active_canvas.itemconfig(self.drag_rect_id, outline="#4caf50", width=2, dash=())
            
            # Show toast/status notification
            self.show_copied_toast(copied_text)
            
            # Delete rectangle after 1 second
            rect_id = self.drag_rect_id
            canvas = self.active_canvas
            self.root.after(1000, lambda: self.safe_delete_rect(canvas, rect_id))
        else:
            # Delete rectangle immediately if no text was found
            self.active_canvas.delete(self.drag_rect_id)
            
        self.drag_rect_id = None
        self.active_canvas = None

    def show_copied_toast(self, text):
        display_text = text if len(text) <= 50 else text[:47] + "..."
        prev_text = self.status_bar_label.cget("text")
        
        self.status_bar.config(bootstyle="success")
        self.status_bar_label.config(bootstyle="inverse-success", text=f"✓ Copied to clipboard: \"{display_text}\"")
        
        if hasattr(self, '_status_reset_id'):
            try:
                self.root.after_cancel(self._status_reset_id)
            except Exception:
                pass
        
        def reset_status():
            self.status_bar.config(bootstyle="secondary")
            self.status_bar_label.config(bootstyle="inverse-secondary", text=prev_text)
            
        self._status_reset_id = self.root.after(2000, reset_status)

    def safe_delete_rect(self, canvas, rect_id):
        try:
            canvas.delete(rect_id)
        except Exception:
            pass

    def process_pdf(self):
        filename = self.pdf_files[self.current_index]
        input_path = os.path.join(self.input_dir, filename)
        
        # Gather data
        loc = self.loc_var.get().strip()
        acc = self.acc_var.get().strip()
        gl = self.gl_var.get().strip()
        desc = self.desc_var.get().strip()
        date_str = self.date_var.get().strip()
        
        if not loc or loc == "Select Location...":
            messagebox.showerror("Error", "Please select a location.")
            return

        if loc != "Split" and (not acc or acc == "Select Account..."):
            messagebox.showerror("Error", "Please select an account.")
            return

        # --- New Renaming Logic ---
        try:
            # Parse mm/dd/yyyy to YYYY-MM-DD for better sorting
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except Exception:
            formatted_date = datetime.now().strftime("%Y-%m-%d")

        # Sanitize charge for the filename
        clean_charge = self.sanitize_filename(self.charge_var.get().strip())
        
        # Construct new filename: [Date] - [Charge].pdf
        if clean_charge:
            new_filename = f"{formatted_date} - {clean_charge}.pdf"
        else:
            # Fallback if charge is empty: use Location and Description as before
            clean_loc = "Split" if loc in ["Split", "Split as per"] else self.sanitize_filename(loc)
            clean_desc = self.sanitize_filename(desc)
            new_filename = f"{formatted_date} - {clean_loc} - {clean_desc}.pdf"
            if not clean_desc:
                new_filename = f"{formatted_date} - {clean_loc}.pdf"
            
        # Dynamically save processed file inside the selected Location's subdirectory within Locations folder
        output_dir = os.path.join(self.output_dir, loc)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, new_filename)
        
        # Handle collision (if file already exists in target folder)
        counter = 1
        while os.path.exists(output_path):
            counter += 1
            base_name = os.path.splitext(new_filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}_{counter}.pdf")
        # --------------------------

        # Build stamp text
        stamp_lines = []
        source = self.source_var.get().strip()
        if loc == "Split":
            total_p = 0.0
            if hasattr(self, 'split_rows') and self.split_rows:
                for row in self.split_rows:
                    l = row["loc"].get()
                    p = row["perc"].get()
                    if l and p and l != "Select...":
                        row_code = ""
                        code_val = self.get_gl_code(l, acc, source)
                        if code_val and code_val != "NA":
                            row_code = f" - {code_val}"
                        stamp_lines.append(f"{l} ({p}%){row_code}")
                        try:
                            total_p += float(p)
                        except ValueError: pass
                if abs(total_p - 100.0) > 0.01:
                    messagebox.showwarning("Split Warning", f"Total percentage is {total_p}%, not 100%. Proceeding anyway.")
            else:
                messagebox.showerror("Error", "Split rows not found. Please select split locations.")
                return
        elif loc in ["Split All", "Split as per"]:
            stamp_lines.append(loc)
            self.last_location = loc
        else:
            stamp_lines.append(f"Location: {loc}")
            if acc and acc != "Select Account...":
                stamp_lines.append(f"Account: {acc}")
            self.last_location = loc

        stamp_text = "\n".join(stamp_lines) + f"\nGL Code: {gl}\nDesc: {desc}\nDate: {date_str}"
        
        # Calculate dynamic box height (roughly 20px per line + padding)
        box_height = (len(stamp_lines) + 3) * 20 + 10 
        
        try:
            doc = self.current_pdf_doc
            page = doc[0]
            
            page_width = page.rect.width
            rect = fitz.Rect(page_width - 320, 30, page_width - 20, 30 + box_height)
            
            # Background
            shape = page.new_shape()
            shape.draw_rect(rect)
            shape.finish(color=(0,0,0), fill=(1,1,1), fill_opacity=0.9, width=1)
            shape.commit()
            
            # Text
            page.insert_textbox(
                rect, 
                stamp_text, 
                fontsize=12, 
                fontname="helv", 
                color=(0, 0, 0), 
                align=0 
            )
            
            doc.save(output_path)
            doc.close()
            self.current_pdf_doc = None
            
            # Move original invoice to Original folder
            try:
                dest_path = os.path.join(self.archive_dir, filename)
                # If target already exists, append timestamp to filename to avoid error
                if os.path.exists(dest_path):
                    ts = datetime.now().strftime("%H%M%S")
                    dest_path = os.path.join(self.archive_dir, f"{os.path.splitext(filename)[0]}_{ts}.pdf")
                
                print(f"Archive Request: Moving '{input_path}' to '{dest_path}'")
                shutil.move(input_path, dest_path)
            except Exception as e:
                print(f"Archive Error: {e}")
                messagebox.showwarning("Archive Warning", f"Could not move original file to Original folder:\n{e}")
            
            # Remove from the list of pending files
            self.pdf_files.pop(self.current_index)
            
            # We don't increment current_index because the list shifted
            self.load_current_pdf()
            
        except Exception as e:
            messagebox.showerror("Error", f"Save Failed: {e}")

    def skip_pdf(self):
        self.current_index += 1
        self.load_current_pdf()
        
    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_pdf()

if __name__ == "__main__":
    BASE_DIR = r"J:\Accounting Marketing\2026"
    if not os.path.exists(BASE_DIR):
        local_mock = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_J_drive")
        if os.path.exists(local_mock):
            BASE_DIR = local_mock
            
    # Root with a sleek theme
    root = tb.Window(themename="darkly")
    root.withdraw() # Hide until month is selected
    
    selector = MonthSelector(root, BASE_DIR)
    root.wait_window(selector)
    
    if selector.result:
        input_f, output_f, archive_f = selector.result
        root.deiconify()
        app = InvoiceStamperApp(root, input_f, output_f, archive_f)
        root.mainloop()
    else:
        root.destroy()
