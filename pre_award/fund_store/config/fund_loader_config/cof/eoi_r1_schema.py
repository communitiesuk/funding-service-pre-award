from fsd_utils import Decision

COF_SECURE_MATCH_FUNDING_CAVEAT_EN = (
    "Make progress in securing match funding: COF will contribute up to 80% of the"
    " capital costs you require, and you must raise at least 20% from other sources."
    " You do not need to have secured all your match funding by the time you apply, but"
    " we will ask you to set out your total costs, funding already secured, and plans"
    " to raise any additional funding. You must use COF funding within 12 months, so"
    " you must be able to show that you've made good progress to secure the remaining"
    " match funding. This is so that we're confident you can draw down this funding"
    " within this timeframe."
)
COF_SECURE_MATCH_FUNDING_CAVEAT_CY = (
    "Gwneud cynnydd i sicrhau arian cyfatebol: Bydd y Gronfa Perchnogaeth Gymunedol yn cyfrannu hyd at 80% o'r costau "
    "cyfalaf sydd eu hangen arnoch, ac mae'n rhaid i chi godi o leiaf 20% o ffynonellau eraill. Nid oes angen i chi "
    "fod wedi sicrhau eich holl arian cyfatebol erbyn i chi wneud cais, ond byddwn yn gofyn i chi nodi cyfanswm eich "
    "costau, y cyllid rydych eisoes wedi'i sicrhau, a chynlluniau i godi unrhyw gyllid ychwanegol. Mae'n rhaid i chi "
    "ddefnyddio cyllid o'r Gronfa Perchnogaeth Gymunedol o fewn 12 mis, felly mae'n rhaid i chi allu dangos eich bod "
    "wedi gwneud cynnydd da i sicrhau'r arian cyfatebol sy'n weddill. Diben hyn yw rhoi'r hyder i ni y gallwch "
    "ddefnyddio'r cyllid hwn o fewn yr amserlen hon."
)


COF_PLANNING_PERMISSION_IF_NEEDED_CAVEAT_EN = (
    "Get planning permission, if needed: When you apply, you must be able to show that you have secured or have made"
    " good progress in securing planning permission, if needed (and building warrants, if required). This is so that"
    " we're confident that COF funding will be used within the 12 month timeframe."
)
COF_PLANNING_PERMISSION_IF_NEEDED_CAVEAT_CY = (
    "Sicrhewch ganiatâd cynllunio, os oes angen: Pan fyddwch yn gwneud cais, rhaid i chi allu dangos eich bod wedi "
    "sicrhau caniatâd cynllunio os oes angen (a gwarantau adeiladu, os oes angen), neu'ch bod wedi gwneud cynnydd da "
    "yn hyn o beth.  Diben hyn yw rhoi'r hyder i ni y caiff cyllid o'r Gronfa Perchnogaeth Gymunedol ei ddefnyddio o "
    "fewn y cyfnod o 12 mis."
)


COF_PLANNING_PERMISSION_CAVEAT_EN = (
    "Get planning permission: When you apply, you must be able to show that you have secured or have made good progress"
    " in securing planning permission (and building warrants, if required). This is so that we're confident that COF"
    " funding will be used within the 12 month timeframe."
)
COF_PLANNING_PERMISSION_CAVEAT_CY = (
    "Sicrhewch ganiatâd cynllunio: Pan fyddwch yn gwneud cais, rhaid i chi allu dangos eich bod wedi sicrhau caniatâd "
    "cynllunio (a gwarantau adeiladu, os oes angen), neu'ch bod wedi gwneud cynnydd da yn hyn o beth. Diben hyn yw "
    "rhoi'r hyder i ni y caiff cyllid o'r Gronfa Perchnogaeth Gymunedol ei ddefnyddio o fewn y cyfnod o 12 mis."
)


COF_R3_EOI_SCHEMA_EN = {
    "uYiLsv": [
        {
            "answerValue": "not-yet-incorporated",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Incorporate your organisation: You must have incorporated your"
                " organisation by the time you submit a full application. If you remain"
                " unincorporated, your application will be ineligible."
            ),
        },
    ],
    "NcQSbU": [
        {
            "answerValue": True,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "eEaDGz": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "zurxox": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "lLQmNb": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "fBhSNc": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "XuAyrs": [
        {
            "answerValue": "Yes, a town, parish or community council",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Understand the rules on acquiring assets from town, parish or"
                " community councils: We cannot fund you to acquire a publicly owned"
                " asset if this involves transferring responsibility for delivering"
                " statutory services (services paid for by tax payers) from the public"
                " authority to your organisation. You should only apply to acquire an"
                " asset from a town, parish or community council if you do not plan to"
                " deliver statutory services."
            ),
        },
        {
            "answerValue": "Yes, another type of public authority",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Understand the rules on acquiring public sector assets: COF funding"
                " can only be used for renovation and refurbishment costs once a"
                " publicly owned asset has been transferred to you. We cannot fund"
                " capital receipts, unless the costs incurred in transferring the asset"
                " to you are nominal (very small and far below the real value).In your"
                " application, you should show that you are not asking COF to fund a"
                " capital receipt to a public authority (for example, by sharing a"
                " letter confirming the authority is willing/has already agreed a"
                " long-term lease and no capital receipt is involved).We also cannot"
                " fund you to acquire a publicly owned asset if this involves"
                " transferring responsibility for delivering statutory services"
                " (services paid for by tax payers) from the public authority to your"
                " organisation"
            ),
        },
    ],
    "foQgiy": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "BykoQQ": [
        {
            "answerValue": ["Not sure"],
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Make progress in securing match funding: COF will contribute up to 80%"
                " of the capital costs you require, and you must raise at least 20%"
                " from other sources.You do not need to have secured all your match"
                " funding by the time you apply, but we will ask you to set out your"
                " total costs, funding already secured, and plans to raise any"
                " additional funding.You must use COF funding within 12 months, so you"
                " must be able to show that you've made good progress to secure the"
                " remaining match funding. This is so that we're confident you can draw"
                " down this funding within this timeframe."
            ),
        },
    ],
    "eOWKoO": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "oblxxv": [
        {
            "answerValue": False,
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Consider requesting revenue funding: We encourage all organisations"
                " to apply for revenue funding to help cover the initial running costs"
                " of your project. When you apply, you'll need to show us how you"
                " plan to use any revenue funding."
                " See [Section 9 of the COF prospectus for more"
                " guidance](https://www.gov.uk/government/publications/community-"
                "ownership-fund-prospectus/community-ownership-fund-prospectus--3#funding-available)."
            ),
        },
    ],
    "kWRuac": [
        {
            "answerValue": "Not yet approached any funders",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT_EN,
        },
        {
            "answerValue": "Approached some funders but not yet secured",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT_EN,
        },
        {
            "answerValue": "Approached all funders but not yet secured",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT_EN,
        },
        {
            "answerValue": "Secured some match funding",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT_EN,
        },
    ],
    "yZxdeJ": [
        {
            "answerValue": True,
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Understand the rules on housing: We will not provide funding if your"
                " project's main purpose is to purchase or develop housing assets,"
                " including social housing. However, you can include housing elements"
                " in your project where these are only a small part of supporting the"
                " overall financial sustainability of the asset in community ownership."
            ),
        }
    ],
    "UORyaF": [
        {
            "answerValue": "Not sure",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_IF_NEEDED_CAVEAT_EN,
        }
    ],
    "jICagT": [
        {
            "answerValue": "Not yet started",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_CAVEAT_EN,
        },
        {
            "answerValue": "Early stage",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_CAVEAT_EN,
        },
    ],
    "fZAMFv": [
        {
            "operator": ">",
            "compareValue": 2000000,  # 2 million
            "result": Decision.FAIL,
            "caveat": None,
        }
    ],
}
COF_R3_EOI_SCHEMA_CY = {
    "uYiLsv": [
        {
            "answerValue": "Ddim yn gorfforedig eto",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Dylech gorffori eich sefydliad: Mae'n rhaid eich bod wedi corffori eich sefydliad erbyn eich bod yn "
                "cyflwyno cais llawn. Os byddwch yn anghorfforedig o hyd, ni fydd eich cais yn gymwys."
            ),
        },
    ],
    "NcQSbU": [
        {
            "answerValue": True,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "eEaDGz": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "zurxox": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "lLQmNb": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "fBhSNc": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "XuAyrs": [
        {
            "answerValue": "Ydy, cyngor tref, plwyf neu gymuned",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Dylech ddeall y rheolau ynglŷn â chaffael asedau gan gynghorau tref, plwyf neu gymuned: Ni allwn "
                "eich ariannu i gaffael ased dan berchnogaeth gyhoeddus os yw'n golygu trosglwyddo cyfrifoldeb am "
                "ddarparu gwasanaethau statudol (gwasanaethau y mae trethdalwyr yn talu amdanynt) o'r awdurdod "
                "cyhoeddus i'ch sefydliad. Dim ond os nad ydych yn bwriadu darparu gwasanaethau statudol y dylech "
                "wneud cais i gaffael ased gan gyngor tref, plwyf neu gymuned."
            ),
        },
        {
            "answerValue": "Ydy, math arall o awdurdod cyhoeddus",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Dylech ddeall y rheolau ynglŷn â chaffael asedau'r sector cyhoeddus: Dim ond ar ôl trosglwyddo ased "
                "sydd dan berchnogaeth gyhoeddus i chi y gellir defnyddio cyllid o'r Gronfa Perchnogaeth Gymunedol ar "
                "gyfer costau adnewyddu ac ailwampio. Ni allwn ariannu derbyniad cyfalaf, oni bai bod y costau yr aed "
                "iddynt wrth drosglwyddo'r ased i chi yn nominal (bach iawn ac yn llawer is na'r gwerth gwirioneddol). "
                "Yn eich cais, dylech ddangos nad ydych yn gofyn i'r Gronfa Perchnogaeth Gymunedol ariannu derbyniad "
                "cyfalaf i awdurdod cyhoeddus (er enghraifft drwy rannu llythyr yn cadarnhau bod yr awdurdod yn fodlon "
                "ar/eisoes wedi cytuno i les hirdymor ac nad oes derbyniad cyfalaf yn gysylltiedig). Ni allwn ychwaith "
                "eich ariannu i gaffael ased dan berchnogaeth gyhoeddus os yw'n golygu trosglwyddo cyfrifoldeb am "
                "ddarparu gwasanaethau statudol (gwasanaethau y mae trethdalwyr yn talu amdanynt) o'r awdurdod "
                "cyhoeddus i'ch sefydliad."
            ),
        },
    ],
    "foQgiy": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "BykoQQ": [
        {
            "answerValue": ["none"],
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Gwneud cynnydd i sicrhau arian cyfatebol: Bydd y Gronfa Perchnogaeth Gymunedol yn cyfrannu hyd at "
                "80% o'r costau cyfalaf sydd eu hangen arnoch, ac mae'n rhaid i chi godi o leiaf 20% o ffynonellau "
                "eraill. Nid oes angen i chi fod wedi sicrhau eich holl arian cyfatebol erbyn i chi wneud cais, "
                "ond byddwn yn gofyn i chi nodi cyfanswm eich costau, y cyllid rydych eisoes wedi'i sicrhau, "
                "a chynlluniau i godi unrhyw gyllid ychwanegol. Mae'n rhaid i chi ddefnyddio cyllid o'r Gronfa "
                "Perchnogaeth Gymunedol o fewn 12 mis, felly mae'n rhaid i chi allu dangos eich bod wedi gwneud "
                "cynnydd da i sicrhau'r arian cyfatebol sy'n weddill. Diben hyn yw rhoi'r hyder i ni y gallwch "
                "ddefnyddio'r cyllid hwn o fewn yr amserlen hon."
            ),
        },
    ],
    "eOWKoO": [
        {
            "answerValue": False,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "oblxxv": [
        {
            "answerValue": False,
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Ystyriwch wneud cais am gyllid refeniw: Rydym yn annog pob sefydliad i wneud cais am gyllid refeniw "
                "er mwyn helpu i dalu costau rhedeg cychwynnol eich prosiect. Pan fyddwch yn gwneud cais, bydd angen "
                "i chi ddangos i ni sut rydych yn bwriadu defnyddio unrhyw gyllid refeniw. [Gweler Adran 9 o "
                "brosbectws y Gronfa Perchnogaeth Gymunedol am ragor o ganllawiau.]("
                "https://www.gov.uk/government/publications/community-ownership-fund-prospectus/community-ownership"
                "-fund-prospectus--3#funding-available)"
            ),
        },
    ],
    "kWRuac": [
        {
            "answerValue": "Heb gysylltu ag unrhyw gyllidwyr eto",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT_CY,
        },
        {
            "answerValue": "Wedi cysylltu â rhai cyllidwyr ond heb sicrhau cyllid eto",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT_CY,
        },
        {
            "answerValue": "Wedi cysylltu â'r holl gyllidwyr ond heb sicrhau cyllid eto",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT_CY,
        },
        {
            "answerValue": "Wedi sicrhau rhywfaint o arian cyfatebol",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT_CY,
        },
    ],
    "yZxdeJ": [
        {
            "answerValue": True,
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Dylech ddeall y rheolau ynglyn â thai: Ni fyddwn yn darparu cyllid os mai prif ddiben eich prosiect "
                "yw prynu neu ddatblygu asedau tai, gan gynnwys tai cymdeithasol. Fodd bynnag, gallwch gynnwys "
                "elfennau tai yn eich prosiect os mai dim ond rhan fach o gefnogi cynaliadwyedd ariannol gyffredinol "
                "yr ased dan berchnogaeth gymunedol yw'r rhain."
            ),
        }
    ],
    "UORyaF": [
        {
            "answerValue": "Ddim yn siŵr",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_IF_NEEDED_CAVEAT_CY,
        }
    ],
    "jICagT": [
        {
            "answerValue": "Heb ddechrau eto",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_CAVEAT_CY,
        },
        {
            "answerValue": "Cam cynnar",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_CAVEAT_CY,
        },
    ],
    "fZAMFv": [
        {
            "operator": ">",
            "compareValue": 2000000,  # 2 million
            "result": Decision.FAIL,
            "caveat": None,
        }
    ],
}
