from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import ChannelsTooMuchError, ChannelInvalidError,\
    ChannelPrivateError


def join_group(client, account, group):
    try:
        client(JoinChannelRequest(group))
        return True
    except ChannelsTooMuchError as e:
        account.deactivate(e.__class__.__name__)
        account.update_last_used()
        return False
    except ChannelInvalidError:
        return {'success': False, 'error': _('Group is Invalid.')}
    except ChannelPrivateError:
        return {'success': False, 'error': _('Group is Private and not '
                                             'accessible.')}
