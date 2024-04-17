insert into ess_mondial.country SELECT * FROM ess_mondial_db.country;
insert into ess_mondial.language SELECT * FROM ess_mondial_db.language;
insert into ess_mondial.representative SELECT * FROM ess_mondial_db.representative;
insert into ess_mondial.client SELECT * FROM ess_mondial_db.client;
insert into ess_mondial.client_contact SELECT * FROM ess_mondial_db.client_contact;
insert into ess_mondial.local_contact SELECT * FROM ess_mondial_db.local_contact;
insert into ess_mondial.project SELECT * FROM ess_mondial_db.project;

insert into ess_mondial.article SELECT * FROM ess_mondial_db.article;
insert into ess_mondial.article_unit SELECT * FROM ess_mondial_db.article_unit;
insert into ess_mondial.supplier SELECT * FROM ess_mondial_db.supplier;

# done 
insert into ess_mondial.shipping SELECT * FROM ess_mondial_db.shipping;
insert into ess_mondial.payment SELECT * FROM ess_mondial_db.payment;
insert into ess_mondial.time_unit SELECT * FROM ess_mondial_db.time_unit;
insert into ess_mondial.transport SELECT * FROM ess_mondial_db.transport;
insert into ess_mondial.destination SELECT * FROM ess_mondial_db.destination;
insert into ess_mondial.currency SELECT * FROM ess_mondial_db.currency;
commit;