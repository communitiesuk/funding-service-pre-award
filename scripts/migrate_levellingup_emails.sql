-- Update any rows in the `round` table that have a contact email address on the levellingup domain to point at the communities domain instead.

SELECT * FROM round WHERE contact_email LIKE '%@levellingup.gov.uk';

UPDATE round SET contact_email = REPLACE(contact_email, '@levellingup.gov.uk', '@communities.gov.uk') WHERE contact_email LIKE '%@levellingup.gov.uk';

SELECT * FROM round WHERE contact_email LIKE '%@levellingup.gov.uk';
