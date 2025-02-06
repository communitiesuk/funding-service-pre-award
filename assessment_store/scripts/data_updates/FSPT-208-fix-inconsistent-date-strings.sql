begin;

/* Check the result is {some} */
select count(*) from assessment_records where jsonb_blob->>'date_submitted' like '%+00.00';

/* Check we've updated {some} */
update assessment_records
set jsonb_blob['date_submitted'] = to_jsonb(replace(jsonb_blob->>'date_submitted', '+00.00', ''))
where jsonb_blob->>'date_submitted' like '%+00.00';

/* Check the result is 0 */
select count(*) from assessment_records where jsonb_blob->>'date_submitted' like '%+00.00';

/* Only commit if everything lined up as expected */
commit;
