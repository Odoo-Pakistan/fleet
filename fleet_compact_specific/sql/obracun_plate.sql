
-- OVDJE TREBA DODATI JOS USLOV DA SE ODABERE MJESEC I VOZAC
select 
	--row_number() OVER (ORDER BY tro.date asc) as "redni_broj",
	tro.date as datum,
	to_char(tro.date, 'MM') as mjesec,
	to_char(tro.date, 'yyyy') as godina,
	res.name as vozac,
	fak.broj_fakture,
	tro.distance as relacija,
	fak.prevezeno_tona,
	fak."cijena_po_toni_EUR",
	(fak.prevezeno_tona*fak."cijena_po_toni_EUR") as "vrijednost_EUR",
	fak.ukupan_iznos as "vrijednost_KM",
	(0.1*fak.ukupan_iznos) as zarada_vozaca
	
from fleet_invoice fak
left join fleet_vehicle_travel_order tro on (tro.id = fak.travel_order_id)
left join hr_employee emp on (emp.id = tro.driver1_id)
left join resource_resource res on (res.id = emp.resource_id)