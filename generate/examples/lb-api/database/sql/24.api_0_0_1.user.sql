\c one_db
SET search_path TO api_0_0_1, base_0_0_1, public;
--
CREATE OR REPLACE FUNCTION api_0_0_1.user(token TEXT,form JSON)  RETURNS JSONB AS $$
    Declare _form JSONB; Declare result JSONB; Declare _chelate JSONB := '{}'::JSONB;Declare tmp TEXT;
BEGIN
          -- [Function: User POST]
          -- [Description: Store the original values of a user chelate]
            -- [Parameters: token TEXT,form JSON]
            -- [pk is <text-value> or guid#<value>
          -- [Switch to api_guest Role]
          set role api_guest; 
          -- [Validate token parameter]
          result := base_0_0_1.validate_token(token) ;
          if result is NULL then
            -- [Fail 403 When token is invalid]
            RESET ROLE;
            return format('{"status":"403","msg":"Forbidden","extra":"Invalid token","user":"%s"}',CURRENT_USER)::JSONB;
          end if;
          -- [Verify token has expected scope]
          if not(result ->> 'scope' = 'api_guest') then
              RESET ROLE;
              -- [Fail 401 when unexpected scope is detected]
              return '{"status":"401","msg":"Unauthorized"}'::JSONB;
          end if; 
-- [Validate form parameter] 
          if form is NULL then
              -- [Fail 400 when form is NULL]
              RESET ROLE;
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;    
          _form := form::JSONB; 
-- [Validate Requred form fields]
          if not(_form ? 'username') or not(_form ? 'password') then  
              -- [Fail 400 when form is missing requrired field]
              RESET ROLE;
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;
        -- [Assemble Data]
        -- [Hash password when found]
        if _form ? 'password' then
            _form := _form || format('{"password": "%s"}',crypt(form ->> 'password', gen_salt('bf')) )::JSONB; 
        end if;  
        -- user specific stuff
          if CURRENT_USER = 'api_guest' then
              -- [Chelate Data]
              _chelate := base_0_0_1.chelate('{"pk":"username","sk":"const#USER","tk":"*"}'::JSONB, _form); -- chelate with keys on insert
              -- [Stash guid for insert]
              tmp = set_config('request.jwt.claim.key', replace(_chelate ->> 'tk','guid#',''), true); 
              -- If is_local is true, the new value will only apply for the current transaction.
              --raise notice 'tmp %', tmp; 
          end if;
          -- [Insert user Chelate]
          result := base_0_0_1.insert(_chelate);
          RESET ROLE;
          -- [Return {status,msg,insertion}]
          return result;    
        END;
        $$ LANGUAGE plpgsql;
grant EXECUTE on FUNCTION api_0_0_1.user(TEXT, JSON) to api_guest;
--
CREATE OR REPLACE FUNCTION api_0_0_1.user(token TEXT,criteria JSON,options JSON)  RETURNS JSONB AS $$
    Declare _criteria JSONB; Declare result JSONB;
BEGIN
          -- [Function: User GET]
          -- [Description: Find the values of a user chelate]
            -- [Parameters: token TEXT,criteria JSON,options JSON]
          -- [Switch to api_guest Role]
          set role api_guest; 
          -- [Validate token parameter]
          result := base_0_0_1.validate_token(token) ;
          if result is NULL then
            -- [Fail 403 When token is invalid]
            RESET ROLE;
            return format('{"status":"403","msg":"Forbidden","extra":"Invalid token","user":"%s"}',CURRENT_USER)::JSONB;
          end if;
          -- [Verify token has expected scope]
          if not(result ->> 'scope' = 'api_user') and not(result ->> 'scope' = 'api_admin') then
              RESET ROLE;
              -- [Fail 401 when unexpected scope is detected]
              return '{"status":"401","msg":"Unauthorized"}'::JSONB;
          end if; 
          -- Validate Criteria
          -- Validate Options
          -- [Assemble user specific data]
          _criteria=criteria::JSONB;
          if CURRENT_USER = 'api_user' then
              if _criteria ? 'pk' and _criteria ? 'sk' then
                  -- [Primary query {pk,sk}]
                  _criteria = format('{"pk":"%s", "sk":"%s"}',_criteria ->> 'pk',_criteria ->> 'sk')::JSONB;
              elsif _criteria ? 'pk' and not(_criteria ? 'sk') then
                   -- [Primary query {pk,sk:*}]
                  _criteria = format('{"pk":"%s", "sk":"%s"}',_criteria ->> 'pk','*')::JSONB;
              elsif _criteria ? 'sk' and _criteria ? 'tk' then
                  -- [Secondary query {sk,tk}]
                  _criteria = format('{"sk":"%s", "tk":"%s"}',_criteria ->> 'sk',_criteria ->> 'tk')::JSONB;
              elsif _criteria ? 'sk' and not(_criteria ? 'tk') then
                  -- [Secondary query {sk,tk:*}]
                  _criteria = format('{"sk":"%s", "tk":"%s"}',_criteria ->> 'sk','*')::JSONB;
              elsif _criteria ? 'xk' and _criteria ? 'yk' then
                  -- [Teriary query {tk,sk} aka {xk, yk}]
                  _criteria = format('{"xk":"%s", "yk":"%s"}',_criteria ->> 'xk',_criteria ->> 'yk')::JSONB;
              elsif _criteria ? 'xk' and not(_criteria ? 'yk') then
                  -- [Teriary query {tk} aka {xk}]
                  _criteria = format('{"xk":"%s", "yk":"%s"}',_criteria ->> 'xk','*')::JSONB;
              elsif _criteria ? 'yk' and _criteria ? 'zk' then
                  -- [Quaternary query {sk,pk} akd {yk,zk}
                  _criteria = format('{"yk":"%s", "zk":"%s"}',_criteria ->> 'yk',_criteria ->> 'zk')::JSONB;
              elsif _criteria ? 'yk' and not(_criteria ? 'zk') then
                  -- [Quaternary query {yk}
                  _criteria = format('{"yk":"%s", "zk":"%s"}',_criteria ->> 'yk','*')::JSONB;                
              end if;
           elsif CURRENT_USER = 'api_admin' then
              if _criteria ? 'pk' and _criteria ? 'sk' then
                  -- [Primary query {pk,sk}]
                  _criteria = format('{"pk":"%s", "sk":"%s"}',_criteria ->> 'pk',_criteria ->> 'sk')::JSONB;
              elsif _criteria ? 'pk' and not(_criteria ? 'sk') then
                   -- [Primary query {pk,sk:*}]
                  _criteria = format('{"pk":"%s", "sk":"%s"}',_criteria ->> 'pk','*')::JSONB;
              elsif _criteria ? 'sk' and _criteria ? 'tk' then
                  -- [Secondary query {sk,tk}]
                  _criteria = format('{"sk":"%s", "tk":"%s"}',_criteria ->> 'sk',_criteria ->> 'tk')::JSONB;
              elsif _criteria ? 'sk' and not(_criteria ? 'tk') then
                  -- [Secondary query {sk,tk:*}]
                  _criteria = format('{"sk":"%s", "tk":"%s"}',_criteria ->> 'sk','*')::JSONB;
              elsif _criteria ? 'xk' and _criteria ? 'yk' then
                  -- [Teriary query {tk,sk} aka {xk, yk}]
                  _criteria = format('{"xk":"%s", "yk":"%s"}',_criteria ->> 'xk',_criteria ->> 'yk')::JSONB;
              elsif _criteria ? 'xk' and not(_criteria ? 'yk') then
                  -- [Teriary query {tk} aka {xk}]
                  _criteria = format('{"xk":"%s", "yk":"%s"}',_criteria ->> 'xk','*')::JSONB;
              elsif _criteria ? 'yk' and _criteria ? 'zk' then
                  -- [Quaternary query {sk,pk} akd {yk,zk}
                  _criteria = format('{"yk":"%s", "zk":"%s"}',_criteria ->> 'yk',_criteria ->> 'zk')::JSONB;
              elsif _criteria ? 'yk' and not(_criteria ? 'zk') then
                  -- [Quaternary query {yk}
                  _criteria = format('{"yk":"%s", "zk":"%s"}',_criteria ->> 'yk','*')::JSONB;                
              end if;
          end if;
          -- [API GET user Function]
          result := base_0_0_1.query(_criteria);
          RESET ROLE;
          -- [Return {status,msg,insertion}]
          return result;    
        END;
        $$ LANGUAGE plpgsql;
grant EXECUTE on FUNCTION api_0_0_1.user(TEXT, JSON, JSON) to api_guest;
--
CREATE OR REPLACE FUNCTION api_0_0_1.user(token TEXT,pk TEXT)  RETURNS JSONB AS $$
    Declare result JSONB; Declare _criteria JSONB := '{}'::JSONB;
BEGIN
          -- [Function: User DELETE]
          -- [Description: Remove a user from the table]
            -- [Parameters: token TEXT,pk TEXT]
            -- [Delete by primary key]
            -- [pk is <text-value> or guid#<value>
          -- [Switch to api_guest Role]
          set role api_guest; 
          -- [Validate token parameter]
          result := base_0_0_1.validate_token(token) ;
          if result is NULL then
            -- [Fail 403 When token is invalid]
            RESET ROLE;
            return format('{"status":"403","msg":"Forbidden","extra":"Invalid token","user":"%s"}',CURRENT_USER)::JSONB;
          end if;
          -- [Verify token has expected scope]
          if not(result ->> 'scope' = 'api_user') then
              RESET ROLE;
              -- [Fail 401 when unexpected scope is detected]
              return '{"status":"401","msg":"Unauthorized"}'::JSONB;
          end if; 
          -- [Validate pk parameter]
          if pk is NULL then
              RESET ROLE;
              -- [Fail 400 when pk is NULL]
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;
          -- [Assemble user specific data]
          if CURRENT_USER = 'api_user' then
              if strpos(pk,'#') > 0 then
                -- [Assume <key> is valid when # is found ... at worst, delete will end with a 404]
                -- [Delete by pk:<key>#<value> and sk:const#USER when undefined prefix]                
                _criteria := format('{"pk":"%s", "sk":"const#USER"}',pk)::JSONB;
              else
                -- [Wrap pk as primary key when # is not found in pk]
                -- [Delete by pk:username#<value> and sk:const#USER when <key># is not present]
                _criteria := format('{"pk":"username#%s", "sk":"const#USER"}',pk)::JSONB;              
              end if;
          end if;
          -- [API DELETE user Function]
          result := base_0_0_1.delete(_criteria);
          RESET ROLE;
          -- [Return {status,msg,insertion}]
          return result;    
        END;
        $$ LANGUAGE plpgsql;
grant EXECUTE on FUNCTION api_0_0_1.user(TEXT, TEXT) to api_guest;
--
CREATE OR REPLACE FUNCTION api_0_0_1.user(token TEXT,pk TEXT,form JSON)  RETURNS JSONB AS $$
    Declare _chelate JSONB := '{}'::JSONB; Declare _criteria JSONB := '{}'::JSONB; _form JSONB := '{}'::JSONB; Declare result JSONB;
BEGIN
          -- [Function: User PUT]
          -- [Description: Change the values of a user chelate]
            -- [Parameters: token TEXT,pk TEXT,form JSON]
            -- [Update by primary key]
            -- [pk is <text-value> or guid#<value>
          -- [Switch to api_guest Role]
          set role api_guest; 
          -- [Validate token parameter]
          result := base_0_0_1.validate_token(token) ;
          if result is NULL then
            -- [Fail 403 When token is invalid]
            RESET ROLE;
            return format('{"status":"403","msg":"Forbidden","extra":"Invalid token","user":"%s"}',CURRENT_USER)::JSONB;
          end if;
          -- [Verify token has expected scope]
          if not(result ->> 'scope' = 'api_user') then
              RESET ROLE;
              -- [Fail 401 when unexpected scope is detected]
              return '{"status":"401","msg":"Unauthorized"}'::JSONB;
          end if; 
          -- [Validate pk parameter]
          if pk is NULL then
              RESET ROLE;
              -- [Fail 400 when pk is NULL]
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;
-- [Validate form parameter] 
          if form is NULL then
              -- [Fail 400 when form is NULL]
              RESET ROLE;
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;    
          _form := form::JSONB; 
-- [Validate Requred form fields]
          -- [No required PUT form fields ]
-- [Validate optional form fields]
          -- [No optional PUT form fields]
        -- [Hash password when found]
        if _form ? 'password' then
            _form := _form || format('{"password": "%s"}',crypt(form ->> 'password', gen_salt('bf')) )::JSONB; 
        end if;  
 
        -- [Assemble user specific data]
          if CURRENT_USER = 'api_user' then
              if strpos(pk,'#') > 0 then
                -- [Assume <key> is valid when # is found ... at worst, delete will end with a 404]
                -- [Delete by pk:<key>#<value> and sk:const#USER when undefined prefix]      
                _criteria := format('{"pk":"%s", "sk":"const#USER"}',pk)::JSONB;
              else
                -- [Wrap pk as primary key when # is not found in pk]
                -- [Delete by pk:username#<value> and sk:const#USER when <key># is not present]
                _criteria := format('{"pk":"username#%s", "sk":"const#USER"}',pk)::JSONB;              
              end if;
              -- merget pk and sk
              _chelate := _chelate || _criteria;
              -- add the provided form
              _chelate := _chelate || format('{"form": %s}',_form)::JSONB;  
          end if;
          -- [API PUT user Function]
          result := base_0_0_1.update(_chelate);
          RESET ROLE;
          -- [Return {status,msg,insertion}]
          return result;    
        END;
        $$ LANGUAGE plpgsql;
grant EXECUTE on FUNCTION api_0_0_1.user(TEXT, TEXT, JSON) to api_guest;