-- clean up all data from seed.sql

delete from base_0_0_1.one
  where pk='username#selectchange@user.com' and sk='const#USER';

delete from base_0_0_1.one
  where pk='username#selectchange@user.com' and sk='const#PASSWORD';

delete from base_0_0_1.one
  where pk='username#selectchange@user.com' and sk='const#NAME';

delete from base_0_0_1.one
  where pk='username#existing@user.com' and sk='const#USER';

delete from base_0_0_1.one
  where pk='username#existing2@user.com' and sk='const#USER';

delete from base_0_0_1.one
  where pk='username#delete1@user.com' and sk='const#USER';

delete from base_0_0_1.one
  where pk='username#delete2@user.com' and sk='const#USER';


delete from base_0_0_1.one
  where sk='const#USER' and tk='username#delete3@user.com' ;

delete from base_0_0_1.one
  where pk='username#update@user.com' and sk='const#USER';

delete from base_0_0_1.one
  where pk='username#flip@user.com' and tk='const#FLIP';
