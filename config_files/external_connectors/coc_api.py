
import os
import coc

if os.environ.get("SC_API_LOGIN"):
    coc_client = coc.login(os.environ.get("SC_API_LOGIN"), os.environ.get("SC_API_PASSWORD"), key_names = "ema_ewb", client = coc.EventsClient, key_count = 8)
else:
    import localtoken
    coc_client = coc.login(localtoken.sc_id, localtoken.sc_pass, key_names="ewb_dev", key_count = 1)