CREATE VIEW "nobelwinners" AS SELECT DISTINCT 
nobelwinner.firstname,
nobelwinner.surname,
nobelwinner.born,
nobelwinner.died,
nobelwinner.gender,
nobelwinner.year,
nobelwinner.category,
organization.name,
address .country,
address.coordinates

FROM nobelwinner
LEFT JOIN organization ON organization.id = nobelwinner.org_id
LEFT JOIN address ON address.id = organization.address_id
