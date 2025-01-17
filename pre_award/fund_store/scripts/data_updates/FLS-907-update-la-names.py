import copy

from sqlalchemy import select

from application_store.db.models.application.applications import Applications
from assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from db import db
from fund_store.db.models.fund import Fund
from fund_store.db.models.round import Round

CODE_TO_NAME_MAP = {
    "S12000033": "Aberdeen City Council",
    "S12000034": "Aberdeenshire Council",
    "E07000223": "Adur District Council",
    "E07000032": "Amber Valley Borough Council",
    "S12000041": "Angus Council",
    "S12000035": "Argyll and Bute Council",
    "E07000224": "Arun District Council",
    "E07000170": "Ashfield District Council",
    "E07000105": "Ashford Borough Council",
    "E07000200": "Babergh District Council",
    "E09000002": "Barking and Dagenham London Borough",
    "E09000003": "Barnet London Borough",
    "E08000016": "Barnsley Metropolitan Borough Council",
    "E07000066": "Basildon Borough Council",
    "E07000084": "Basingstoke and Deane Borough Council",
    "E07000171": "Bassetlaw District Council",
    "E06000022": "Bath and North East Somerset Council",
    "E06000055": "Bedford UA",
    "E09000004": "Bexley London Borough",
    "E08000025": "Birmingham City Council",
    "E07000129": "Blaby District Council",
    "E06000008": "Blackburn with Darwen Borough Council",
    "E06000009": "Blackpool Borough Council",
    "W06000019": "Blaenau Gwent County Borough Council",
    "E07000033": "Bolsover District Council",
    "E08000001": "Bolton Metropolitan Borough Council",
    "E07000136": "Boston Borough Council",
    "E06000058": "Bournemouth, Christchurch and Poole (UA)",
    "E06000036": "Bracknell Forest Council",
    "E07000067": "Braintree District Council",
    "E07000143": "Breckland District Council",
    "E09000005": "Brent London Borough",
    "E07000068": "Brentwood Borough Council",
    "W06000013": "Bridgend County Borough Council",
    "E06000043": "Brighton and Hove City Council",
    "E06000023": "Bristol City Council",
    "E07000144": "Broadland District Council",
    "E09000006": "Bromley London Borough",
    "E07000234": "Bromsgrove District Council",
    "E07000095": "Broxbourne Borough Council",
    "E07000172": "Broxtowe Borough Council",
    "E06000060": "Buckinghamshire UA",
    "E07000117": "Burnley Borough Council",
    "E08000002": "Bury Metropolitan Borough Council",
    "W06000018": "Caerphilly County Borough Council",
    "E08000033": "Calderdale Metropolitan Borough Council",
    "E07000008": "Cambridge City Council",
    "E47000008": "Cambridge and Peterborough Combined Authority",
    "E10000003": "Cambridgeshire County Council",
    "E09000007": "Camden London Borough",
    "E07000192": "Cannock Chase District Council",
    "E07000106": "Canterbury City Council",
    "W06000015": "Cardiff Council",
    "W06000010": "Carmarthenshire County Council",
    "E07000069": "Castle Point Borough Council",
    "E06000056": "Central Bedfordshire UA",
    "W06000008": "Ceredigion County Council",
    "E07000130": "Charnwood Borough Council",
    "E07000070": "Chelmsford City Council",
    "E07000078": "Cheltenham Borough Council",
    "E07000177": "Cherwell District Council",
    "E06000049": "Cheshire East UA",
    "E06000050": "Cheshire West and Chester UA",
    "E07000034": "Chesterfield Borough Council",
    "E07000225": "Chichester District Council",
    "E07000118": "Chorley Borough Council",
    "E08000032": "City of Bradford Metropolitan District Council",
    "S12000036": "City of Edinburgh Council",
    "E09000001": "City of London",
    "E06000014": "City of York Council",
    "S12000005": "Clackmannanshire Council",
    "E07000071": "Colchester Borough Council",
    "S12000013": "Comhairle nan Eilean Siar",
    "W06000003": "Conwy County Borough Council",
    "E06000052": "Cornwall County UA",
    "E07000079": "Cotswold District Council",
    "E08000026": "Coventry City Council",
    "E07000226": "Crawley Borough Council",
    "E09000008": "Croydon London Borough",
    "E06000063": "Cumberland Council",
    "E07000096": "Dacorum Borough Council",
    "E06000005": "Darlington Borough Council",
    "E07000107": "Dartford Borough Council",
    "W06000004": "Denbighshire County Council",
    "E06000015": "Derby City Council",
    "E10000007": "Derbyshire County Council",
    "E07000035": "Derbyshire Dales District Council",
    "E10000008": "Devon County Council",
    "E08000017": "Doncaster Metropolitan Borough Council",
    "E06000059": "Dorset Council (UA)",
    "E07000108": "Dover District Council",
    "E08000027": "Dudley Metropolitan Borough Council",
    "S12000006": "Dumfries and Galloway Council",
    "S12000042": "Dundee City Council",
    "E06000047": "Durham County UA",
    "E09000009": "Ealing London Borough",
    "S12000008": "East Ayrshire Council",
    "E07000009": "East Cambridgeshire District Council",
    "E07000040": "East Devon District Council",
    "S12000045": "East Dunbartonshire Council",
    "E07000085": "East Hampshire District Council",
    "E07000242": "East Hertfordshire District Council",
    "E07000137": "East Lindsey District Council",
    "S12000010": "East Lothian Council",
    "E47000013": "East Midlands Combined County Authority",
    "S12000011": "East Renfrewshire Council",
    "E06000011": "East Riding of Yorkshire Council",
    "E07000193": "East Staffordshire Borough Council",
    "E07000244": "East Suffolk Council",
    "E10000011": "East Sussex County Council",
    "E07000061": "Eastbourne Borough Council",
    "E07000086": "Eastleigh Borough Council",
    "E07000207": "Elmbridge Borough Council",
    "E09000010": "Enfield London Borough",
    "E07000072": "Epping Forest District Council",
    "E07000208": "Epsom and Ewell Borough Council",
    "E07000036": "Erewash Borough Council",
    "E10000012": "Essex County Council",
    "E07000041": "Exeter City Council",
    "S12000014": "Falkirk Council",
    "E07000087": "Fareham Borough Council",
    "E07000010": "Fenland District Council",
    "S12000047": "Fife Council",
    "W06000005": "Flintshire County Council",
    "E07000112": "Folkestone and Hythe District Council",
    "E07000080": "Forest of Dean District Council",
    "E07000119": "Fylde Borough Council",
    "E08000037": "Gateshead Metropolitan Borough Council",
    "E07000173": "Gedling Borough Council",
    "S12000049": "Glasgow City Council",
    "E07000081": "Gloucester City Council",
    "E10000013": "Gloucestershire County Council",
    "E07000088": "Gosport Borough Council",
    "E07000109": "Gravesham Borough Council",
    "E07000145": "Great Yarmouth Borough Council",
    "E47000001": "Greater Manchester Combined Authority",
    "E09000011": "Greenwich London Borough",
    "E07000209": "Guildford Borough Council",
    "W06000002": "Gwynedd Council",
    "E09000012": "Hackney London Borough",
    "E06000006": "Halton Borough Council",
    "E09000013": "Hammersmith and Fulham London Borough",
    "E10000014": "Hampshire County Council",
    "E07000131": "Harborough District Council",
    "E09000014": "Haringey London Borough",
    "E07000073": "Harlow District Council",
    "E09000015": "Harrow London Borough",
    "E07000089": "Hart District Council",
    "E06000001": "Hartlepool Borough Council",
    "E07000062": "Hastings Borough Council",
    "E07000090": "Havant Borough Council",
    "E09000016": "Havering London Borough",
    "E06000019": "Herefordshire Council",
    "E10000015": "Hertfordshire County Council",
    "E07000098": "Hertsmere Borough Council",
    "E07000037": "High Peak Borough Council",
    "S12000017": "Highland Council",
    "E09000017": "Hillingdon London Borough",
    "E07000132": "Hinckley and Bosworth Borough Council",
    "E07000227": "Horsham District Council",
    "E09000018": "Hounslow London Borough",
    "E06000010": "Hull City Council",
    "E07000011": "Huntingdonshire District Council",
    "E07000120": "Hyndburn Borough Council",
    "S12000018": "Inverclyde Council",
    "E07000202": "Ipswich Borough Council",
    "W06000001": "Isle of Anglesey County Council",
    "E06000046": "Isle of Wight Council",
    "E06000053": "Isles of Scilly Council",
    "E09000019": "Islington London Borough",
    "E09000020": "Kensington and Chelsea Royal Borough",
    "E10000016": "Kent County Council",
    "E07000146": "King's Lynn and West Norfolk Borough Council",
    "E09000021": "Kingston upon Thames Royal Borough",
    "E08000034": "Kirklees Council",
    "E08000011": "Knowsley Metropolitan Borough Council",
    "E09000022": "Lambeth London Borough",
    "E10000017": "Lancashire County Council",
    "E07000121": "Lancaster City Council",
    "E08000035": "Leeds City Council",
    "E06000016": "Leicester City Council",
    "E10000018": "Leicestershire County Council",
    "E07000063": "Lewes District Council",
    "E09000023": "Lewisham London Borough",
    "E07000194": "Lichfield District Council",
    "E07000138": "Lincoln City Council",
    "E10000019": "Lincolnshire County Council",
    "E08000012": "Liverpool City Council",
    "E47000004": "Liverpool City Region Combined Authority",
    "E09000027": "London Borough of Richmond upon Thames",
    "E06000032": "Luton Borough Council",
    "E07000110": "Maidstone Borough Council",
    "E07000074": "Maldon District Council",
    "E07000235": "Malvern Hills District Council",
    "E08000003": "Manchester City Council",
    "E07000174": "Mansfield District Council",
    "E06000035": "Medway Council",
    "E07000133": "Melton Borough Council",
    "W06000024": "Merthyr Tydfil County Borough Council",
    "E09000024": "Merton London Borough",
    "E07000042": "Mid Devon District Council",
    "E07000203": "Mid Suffolk District Council",
    "E07000228": "Mid Sussex District Council",
    "E06000002": "Middlesbrough Council",
    "S12000019": "Midlothian Council",
    "E06000042": "Milton Keynes Council",
    "E07000210": "Mole Valley District Council",
    "W06000021": "Monmouthshire County Council",
    "S12000020": "Moray Council",
    "ERROR404": "Muckinghamshire Borough UA",
    "W06000012": "Neath Port Talbot County Borough",
    "E07000091": "New Forest District Council",
    "E07000175": "Newark and Sherwood District Council",
    "E08000021": "Newcastle City Council",
    "E07000195": "Newcastle-under-Lyme Borough Council",
    "E09000025": "Newham London Borough",
    "W06000022": "Newport City Council",
    "E10000020": "Norfolk County Council",
    "S12000021": "North Ayrshire Council",
    "E07000043": "North Devon District Council",
    "E07000038": "North East Derbyshire District Council",
    "E06000012": "North East Lincolnshire Council",
    "E47000014": "North East Mayoral Combined Authority (Post May 2024)",
    "E07000099": "North Hertfordshire District Council",
    "E07000139": "North Kesteven District Council",
    "S12000050": "North Lanarkshire Council",
    "E06000013": "North Lincolnshire Council",
    "E07000147": "North Norfolk District Council",
    "E06000061": "North Northamptonshire Council",
    "E06000024": "North Somerset Council",
    "E08000022": "North Tyneside Council",
    "E07000218": "North Warwickshire Borough Council",
    "E07000134": "North West Leicestershire District Council",
    "E06000065": "North Yorkshire Council (UA)",
    "E47000011": "North of Tyne Combined Authority",
    "E06000057": "Northumberland County UA",
    "E07000148": "Norwich City Council",
    "E06000018": "Nottingham City Council",
    "E10000024": "Nottinghamshire County Council",
    "E07000219": "Nuneaton and Bedworth Borough Council",
    "E07000135": "Oadby and Wigston Borough Council",
    "E08000004": "Oldham Metropolitan Borough Council",
    "S12000023": "Orkney Islands Council",
    "E07000178": "Oxford City Council",
    "E10000025": "Oxfordshire County Council",
    "W06000009": "Pembrokeshire County Council",
    "E07000122": "Pendle Borough Council",
    "S12000048": "Perth & Kinross Council",
    "E06000031": "Peterborough City Council",
    "E06000026": "Plymouth City Council",
    "E06000044": "Portsmouth City Council",
    "W06000023": "Powys County Council",
    "E07000123": "Preston City Council",
    "E06000038": "Reading Borough Council",
    "E09000026": "Redbridge London Borough",
    "E06000003": "Redcar and Cleveland Borough Council",
    "E07000236": "Redditch Borough Council",
    "E07000211": "Reigate and Banstead Borough Council",
    "S12000038": "Renfrewshire Council",
    "W06000016": "Rhondda Cynon Taf County Borough Council",
    "E07000124": "Ribble Valley Borough Council",
    "E08000005": "Rochdale Metropolitan Borough Council",
    "E07000075": "Rochford District Council",
    "E07000125": "Rossendale Borough Council",
    "E07000064": "Rother District Council",
    "E08000018": "Rotherham Metropolitan Borough Council",
    "E07000220": "Rugby Borough Council",
    "E07000212": "Runnymede Borough Council",
    "E07000176": "Rushcliffe Borough Council",
    "E07000092": "Rushmoor Borough Council",
    "E06000017": "Rutland County Council",
    "E08000006": "Salford City Council",
    "E08000028": "Sandwell Metropolitan Borough Council",
    "S12000026": "Scottish Borders Council",
    "E08000014": "Sefton Metropolitan Borough Council",
    "E07000111": "Sevenoaks District Council",
    "E08000019": "Sheffield City Council",
    "S12000027": "Shetland Islands Council",
    "E06000051": "Shropshire County UA",
    "E06000039": "Slough Borough Council",
    "E08000029": "Solihull Metropolitan Borough Council",
    "E06000066": "Somerset Council (UA)",
    "S12000028": "South Ayrshire Council",
    "E07000012": "South Cambridgeshire District Council",
    "E07000039": "South Derbyshire District Council",
    "E06000025": "South Gloucestershire Council",
    "E07000044": "South Hams District Council",
    "E07000140": "South Holland District Council",
    "E07000141": "South Kesteven District Council",
    "S12000029": "South Lanarkshire Council",
    "E07000149": "South Norfolk Council",
    "E07000179": "South Oxfordshire District Council",
    "E07000126": "South Ribble Borough Council",
    "E07000196": "South Staffordshire Council",
    "E08000023": "South Tyneside Council",
    "E47000002": "South Yorkshire Mayoral Combined Authority",
    "E06000045": "Southampton City Council",
    "E06000033": "Southend-on-Sea City Council",
    "E09000028": "Southwark London Borough",
    "E07000213": "Spelthorne Borough Council",
    "E07000240": "St Albans City and District Council",
    "E08000013": "St Helens Council",
    "E07000197": "Stafford Borough Council",
    "E10000028": "Staffordshire County Council",
    "E07000198": "Staffordshire Moorlands District Council",
    "E07000243": "Stevenage Borough Council",
    "S12000030": "Stirling Council",
    "E08000007": "Stockport Metropolitan Borough Council",
    "E06000004": "Stockton-on-Tees Borough Council",
    "E06000021": "Stoke-on-Trent City Council",
    "E07000221": "Stratford-on-Avon District Council",
    "E07000082": "Stroud District Council",
    "E10000029": "Suffolk County Council",
    "E08000024": "Sunderland City Council",
    "E10000030": "Surrey County Council",
    "E07000214": "Surrey Heath Borough Council",
    "E09000029": "Sutton London Borough",
    "E07000113": "Swale Borough Council",
    "W06000011": "Swansea Council",
    "E06000030": "Swindon Borough Council",
    "E08000008": "Tameside Metropolitan Borough Council",
    "E07000199": "Tamworth Borough Council",
    "E07000215": "Tandridge District Council",
    "E47000006": "Tees Valley Combined Authority",
    "E07000045": "Teignbridge District Council",
    "E06000020": "Telford and Wrekin Council",
    "E07000076": "Tendring District Council",
    "E07000093": "Test Valley Borough Council",
    "E07000083": "Tewkesbury Borough Council",
    "E07000114": "Thanet District Council",
    "E07000102": "Three Rivers District Council",
    "E06000034": "Thurrock Council",
    "E07000115": "Tonbridge and Malling Borough Council",
    "E06000027": "Torbay Council",
    "W06000020": "Torfaen County Borough",
    "E07000046": "Torridge District Council",
    "E09000030": "Tower Hamlets London Borough",
    "E08000009": "Trafford Metropolitan Borough Council",
    "E07000116": "Tunbridge Wells Borough Council",
    "E07000077": "Uttlesford District Council",
    "W06000014": "Vale of Glamorgan Council",
    "E07000180": "Vale of White Horse District Council",
    "E08000036": "Wakefield Metropolitan District Council",
    "E08000030": "Walsall Metropolitan Borough Council",
    "E09000031": "Waltham Forest London Borough",
    "E09000032": "Wandsworth London Borough",
    "E06000007": "Warrington Borough Council",
    "E07000222": "Warwick District Council",
    "E10000031": "Warwickshire County Council",
    "E07000103": "Watford Borough Council",
    "E07000216": "Waverley Borough Council",
    "E07000065": "Wealden District Council",
    "E07000241": "Welwyn Hatfield Borough Council",
    "E06000037": "West Berkshire Council",
    "E07000047": "West Devon Borough Council",
    "S12000039": "West Dunbartonshire Council",
    "E07000127": "West Lancashire Borough Council",
    "E07000142": "West Lindsey District Council",
    "S12000040": "West Lothian Council",
    "E47000007": "West Midlands Combined Authority",
    "E06000062": "West Northamptonshire Council",
    "E07000181": "West Oxfordshire District Council",
    "E07000245": "West Suffolk Council",
    "E10000032": "West Sussex County Council",
    "E47000003": "West Yorkshire Combined Authority",
    "E47000009": "West of England Combined Authority",
    "E09000033": "Westminster City Council",
    "E06000064": "Westmorland and Furness Council",
    "E08000010": "Wigan Metropolitan Borough Council",
    "E06000054": "Wiltshire County UA",
    "E07000094": "Winchester City Council",
    "E06000040": "Windsor and Maidenhead Royal Borough Council",
    "E08000015": "Wirral Borough Council",
    "E07000217": "Woking Borough Council",
    "E06000041": "Wokingham Borough Council",
    "E08000031": "Wolverhampton City Council",
    "E07000237": "Worcester City Council",
    "E10000034": "Worcestershire County Council",
    "E07000229": "Worthing Borough Council",
    "W06000006": "Wrexham County Borough Council",
    "E07000238": "Wychavon District Council",
    "E07000128": "Wyre Borough Council",
    "E07000239": "Wyre Forest District Council",
    "E47000012": "York and North Yorkshire Mayoral Combined Authority",
}

LPDF_R1 = "f1d514da-0282-4a96-82c4-25c09645d0b0"
GBRF_R1 = "e480f03f-e3e0-4bd0-9026-dfed52cc3982"


def update_local_authority_name(commit: bool = False):  # noqa: C901
    print("\nFetching rounds...")
    rounds = db.session.scalars(select(Round).where(Round.id.in_([LPDF_R1, GBRF_R1]))).all()
    for round in rounds:
        fund = db.session.scalars(select(Fund).where(Fund.id.in_([round.fund_id]))).one()
        print(f"\n\nRound: {round.id}, {fund.short_name}")

        applications = db.session.scalars(select(Applications).where(Applications.round_id == str(round.id))).all()

        print(f"\n\n{fund.short_name} Applications count: {len(applications)}\n")
        for application in applications:
            print(f"\nApplication: {application.id}, {application.project_name}")

            if application.project_name in CODE_TO_NAME_MAP:
                print(
                    f"Application.project_name: '{application.project_name}' ->",
                    f"replacing with: '{CODE_TO_NAME_MAP[application.project_name]}'",
                )
                application.project_name = CODE_TO_NAME_MAP[application.project_name]
            else:
                print(f"Application.project_name not found: {application.project_name}")

            for form in application.forms:
                if form.name not in [
                    "local-plans-local-authority-details-signed-off",
                    "local-plans-local-authority-details",
                ]:
                    continue

                new_json = form.json
                for category in new_json:
                    for field in category["fields"]:
                        if field["key"] not in ["RoLhhf", "OlCBjB"]:
                            continue

                        if field["answer"] in CODE_TO_NAME_MAP:
                            print(
                                f"Form.answer: {field['answer']} ",
                                f"replacing with: {CODE_TO_NAME_MAP[field['answer']]}",
                            )
                            field["answer"] = CODE_TO_NAME_MAP[field["answer"]]
                        else:
                            print(f"From answer not found: {field['key']}, {field['answer']}")

                # update the json
                form.json = new_json

        assessment_records = db.session.scalars(
            select(AssessmentRecord).where(AssessmentRecord.fund_id.in_([round.fund_id]))
        ).all()
        print(f"\n\n{fund.short_name} AssessmentRecord count: {len(assessment_records)}\n")

        for assessment_record in assessment_records:
            project_name = assessment_record.project_name
            json_project_name = assessment_record.jsonb_blob["project_name"]

            print(f"\nAssessmentRecord: {assessment_record.application_id}, {project_name}")
            if project_name in CODE_TO_NAME_MAP:
                print(
                    f"AssessmentRecord.project_name: {project_name} ",
                    f"replacing with: {CODE_TO_NAME_MAP[project_name]}",
                )
                assessment_record.project_name = CODE_TO_NAME_MAP[project_name]
            else:
                print(f"AssessmentRecord.project_name not found: {project_name}")

            new_json_2 = copy.deepcopy(assessment_record.jsonb_blob)

            print(
                f"AssessmentRecord.json_project_name: {assessment_record.application_id},",
                f"{json_project_name}",
            )
            if json_project_name in CODE_TO_NAME_MAP:
                print(
                    f"AssessmentRecord.json_project_name: {json_project_name} ",
                    f"replacing with: {CODE_TO_NAME_MAP[json_project_name]}",
                )
                new_json_2["project_name"] = CODE_TO_NAME_MAP[json_project_name]
            else:
                print(f"AssessmentRecord.json_project_name not found: {json_project_name}")

            for form in new_json_2["forms"]:
                if form["name"] not in [
                    "local-plans-local-authority-details-signed-off",
                    "local-plans-local-authority-details",
                ]:
                    continue

                for question in form["questions"]:
                    for field in question["fields"]:
                        if field["key"] not in ["RoLhhf", "OlCBjB"]:
                            continue

                        if field["answer"] in CODE_TO_NAME_MAP:
                            print(
                                f"Form.answer: {field['answer']} ->",
                                f"replacing with: {CODE_TO_NAME_MAP[field['answer']]}",
                            )
                            field["answer"] = CODE_TO_NAME_MAP[field["answer"]]
                        else:
                            print(f"From answer not found: {field['key']}, {field['answer']}")

            # update the json
            assessment_record.jsonb_blob = new_json_2

    if commit:
        db.session.commit()


def main():
    update_local_authority_name(commit=False)

    # ask for confirmation
    if input("Commit changes? (y/n): ").lower() == "y":
        update_local_authority_name(commit=True)


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
