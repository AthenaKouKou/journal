"""
Endpoints for journal management.
"""
from http import HTTPStatus

from urllib.parse import unquote

from flask import request
from flask_restx import Namespace, Resource, fields

import werkzeug.exceptions as wz
import werkzeug

from backendcore.common.constants import (
    AUTH,
    # CODE,
)

import backendcore.api.common as acmn
from backendcore.api.constants import (
    ADD_FILE,
    CREATE,
    DELETE,
    FIELDS,
    FORM,
    JOURNAL,
    MESSAGE,
    READ,
    RETRIEVE,
    UPDATE,
)

import backendcore.security.sec_manager2 as sm

from backendcore.users.query import fetch_id_by_auth_key


from journal_common.constants import (
    MASTHEAD,
)
import manuscripts.fields as mflds
import manuscripts.add_form as mafrm
import manuscripts.query as mqry
import manuscripts.dashboard as mdsh
import people.fields as pflds
import people.form as pfrm
import people.query as pqry
import people.roles as rls
import text.fields as tflds
from text.fields import (
    EDITOR,
    TEXT,
)
import text.form as tform
import text.query as tqry

from manuscripts.fields import (
    ABSTRACT,
    AUTHORS,
    TITLE,
    WCOUNT,
)

from manuscripts.states import (
    get_state_choices,
    get_action_choices,
)

api = Namespace(JOURNAL, 'Web-based journal manager.')
parser = api.parser()
parser.add_argument(AUTH, location='headers')
MANU = 'manuscripts'
MANU_ID = 'manuscript id'
STATE = 'state'
ACTION = 'action'
DASHCOLUMNS = 'dashcolumns'

PROTOCOL_NM = sm.fetch_journal_protocol_name()


def _get_user_info(request):
    user_id = None
    if request.json:
        user_id = request.json.get(EDITOR)
    auth_key = acmn.get_auth_key_from_request(request)
    if not user_id:
        user_id = fetch_id_by_auth_key(auth_key)
    return user_id, auth_key


#############
# Text
#############

JOURNAL_TEXT_FIELDS = 'Journal text fields'


@api.route(f'/{TEXT}/{FIELDS}')
class TextFields(Resource):
    """
    Get the journal text fields.
    """
    def get(self):
        """
        Get the journal text fields.
        """
        return {JOURNAL_TEXT_FIELDS: tflds.get_flds()}


JOURNAL_TEXT_FORM = 'Journal text add/query/update form'


@api.route(f'/{TEXT}/{FORM}')
class TextForm(Resource):
    """
    Get the form for querying the journal text data.
    """
    def get(self):
        """
        Get the form for querying the journal text data.
        """
        return {JOURNAL_TEXT_FORM: tform.get_form()}


JOURNAL_TEXT_READ = 'Journal text map'


@api.route(f'/{TEXT}/{READ}')
class TextRead(Resource):
    """
    This endpoint serves journal text data as a dict.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Data not found')
    def get(self):
        """
        Returns journal text data.
        """
        texts = tqry.fetch_dict()
        return {JOURNAL_TEXT_READ: texts}


UPDATE_TEXT_FLDS = api.model('UpdateText', {
    TEXT: fields.String,
    EDITOR: fields.String,
})


@api.route(f'/{TEXT}/{UPDATE}/<title>')
@api.expect(parser)
class TextUpdate(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Person not found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(UPDATE_TEXT_FLDS)
    def put(self, title):
        text = request.json.get(TEXT)
        if not text:
            raise wz.NotAcceptable('You must pass text to update.')
        editor, auth_key = _get_user_info(request)
        if not sm.is_permitted(PROTOCOL_NM, sm.UPDATE, user_id=editor,
                               auth_key=auth_key):
            raise wz.Forbidden('Action not permitted.')
        try:
            tqry.update(title, text, editor)
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        return {MESSAGE: 'Text updated.'}


@api.route(f'/{TEXT}/{DELETE}/<title>')
@api.expect(parser)
class TextDelete(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Person not found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(api.model('Placeholder', {}))
    def delete(self, title):
        editor, auth_key = _get_user_info(request)
        if not sm.is_permitted(PROTOCOL_NM, sm.DELETE, user_id=editor,
                               auth_key=auth_key):
            raise wz.Forbidden('Action not permitted.')
        try:
            tqry.delete(title)
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        return {MESSAGE: 'Text updated.'}


#############
# Manuscripts
#############

JOURNAL_MANU_FIELDS = 'Journal manuscript fields'


@api.route(f'/{MANU}/{FIELDS}')
class ManuFields(Resource):
    """
    Get the journal manuscript fields
    """
    def get(self):
        """
        Get the journal manuscript fields
        """
        return {JOURNAL_MANU_FIELDS: mflds.get_flds()}


JOURNAL_MANU_CREATE_FORM = 'Journal manuscript form'


@api.route(f'/{MANU}/{CREATE}/{FORM}')
class ManuCreateForm(Resource):
    """
    Get the form for adding the journal manuscript data.
    """
    def get(self):
        """
        Get the form for adding the journal manuscript data.
        """
        return {JOURNAL_MANU_CREATE_FORM: mafrm.get_form()}


JOURNAL_MANU_READ = 'Journal manuscript map'


@api.route(f'/{MANU}/{READ}')
class ManuRead(Resource):
    """
    This endpoint serves journal manuscript data as a dict.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Data not found')
    def get(self):
        """
        Returns journal manuscript data.
        """
        manuscripts = mqry.fetch_dict()
        return {JOURNAL_MANU_READ: manuscripts}


MANU_AUTHORS_NESTED = api.model('JournalManuAddAuthorsNested', {
    pflds.NAME: fields.String,
    pflds.EMAIL: fields.String,
})


MANU_CREATE_FLDS = api.model('JournalManuAdd', {
    TITLE: fields.String,
    WCOUNT: fields.Integer,
    AUTHORS: fields.List(fields.Nested(MANU_AUTHORS_NESTED)),
    TEXT: fields.String,
    ABSTRACT: fields.String,
})


@api.route(f'/{MANU}/{CREATE}')
class ManuCreate(Resource):
    """
    Create a new journal manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_CREATE_FLDS)
    def put(self):
        try:
            jdata = request.json
            print(f'{jdata=}')
            ret = mqry.add(jdata)
        except Exception as err:
            print(err)
            raise wz.NotAcceptable(f'Manuscript creation error: {err}')
        return {MANU_ID: ret}


file_parser = api.parser()
file_parser.add_argument(mafrm.MANU_FILE,
                         type=werkzeug.datastructures.FileStorage,
                         location='files')


@api.route(f'/{MANU}/{ADD_FILE}/<manu_id>')
class ManuAddFile(Resource):
    """
    Create a new journal manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(file_parser)
    def put(self, manu_id):
        try:
            files = request.files
            mqry.add_file(manu_id, files.to_dict())
        except Exception as err:
            print(err)
            raise wz.NotAcceptable(f'Manuscript creation error: {err}')
        return {MESSAGE: 'File added!'}


NEW_STATE = 'New state'
ACTION = 'action'
RECEIVE_ACTION = 'receive_action'

RECEIVE_ACTION_FLDS = api.model('ReceiveAction', {
    ACTION: fields.String,
    EDITOR: fields.String,
})


@api.route(f'/{MANU}/{RECEIVE_ACTION}/<manu_id>')
@api.expect(parser)
class ManuReceiveAction(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Entry not found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(RECEIVE_ACTION_FLDS)
    def put(self, manu_id):
        action = request.json.get(ACTION)
        if not action:
            raise wz.NotAcceptable('You must pass an action.')
        editor = request.json.get(EDITOR)
        if not editor:
            raise wz.NotAcceptable('You must pass an editor.')
        user_id, auth_key = _get_user_info(request)
        if not sm.is_permitted(PROTOCOL_NM, sm.UPDATE, user_id=editor,
                               auth_key=auth_key):
            raise wz.Forbidden('Action not permitted.')

        referee = request.json.get(mqry.REFEREE_ARG)
        state = request.json.get(mqry.STATE)
        try:
            new_state = mqry.receive_action(manu_id, action,
                                            **{EDITOR: editor,
                                               mqry.REFEREE_ARG: referee,
                                               mqry.STATE: state})
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        return {NEW_STATE: new_state}


@api.route(f'/{MANU}/{DELETE}/<manu_id>')
@api.expect(parser)
class ManuDelete(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Entry not found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(api.model('Placeholder', {}))
    def put(self,  manu_id):
        user_id, auth_key = _get_user_info(request)
        if not sm.is_permitted(PROTOCOL_NM, sm.UPDATE, user_id=user_id,
                               auth_key=auth_key):
            raise wz.Forbidden('Action not permitted.')
        try:
            mqry.delete(manu_id)
            return {MESSAGE: 'Manuscript deleted!'}
        except ValueError:
            print(f'Manuscript not found: {manu_id}.')
            raise wz.NotFound(f'Person not found: {manu_id}')


JOURNAL_MANU_STATES_READ = 'Journal manuscript states choices map'


@api.route(f'/{MANU}/{STATE}/{READ}')
class ManuStatesRead(Resource):
    """
    This endpoint serves journal manuscript states as a dict
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Data not found')
    def get(self):
        """
        Returns journal manuscript state data.
        """
        return {JOURNAL_MANU_STATES_READ: get_state_choices()}


JOURNAL_MANU_ACTIONS_READ = 'Journal manuscript action choices map'


@api.route(f'/{MANU}/{ACTION}/{READ}')
class ManuActionsRead(Resource):
    """
    This endpoint serves journal manuscript actions as a dict
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Data not found')
    def get(self):
        """
        Returns journal manuscript action data.
        """
        return {JOURNAL_MANU_ACTIONS_READ: get_action_choices()}


JOURNAL_MANU_FETCH_STATE = 'Fetch journal manuscript by state'


@api.route(f'/{MANU}/{STATE}/{RETRIEVE}/<state_code>')
class ManuStateFetch(Resource):
    """
    This endpoint returns journal manuscripts that have a given state
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Data not found')
    def get(self, state_code):
        """
        Returns journal manuscripts with a given state.
        """
        return mqry.fetch_by_state(state_code)


JOURNAL_MANU_COLUMNS_READ = "map"
JOURNAL_MANU_COLUMNS_ORDER = "order"


@api.route(f'/{MANU}/{DASHCOLUMNS}/{READ}')
class DashColumnsRead(Resource):
    """
    This endpoint serves journal manuscript dashboard columns as a dict, as
    well as the order the columns should be displayed in as a list.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Data not found')
    def get(self):
        """
        Returns journal manuscript dashboard columns data.
        """
        return {JOURNAL_MANU_COLUMNS_READ: mdsh.get_choices(),
                JOURNAL_MANU_COLUMNS_ORDER: mdsh.get_choices_order()}


#############
# People
#############

PEOPLE = 'people'
PEOPLE_FIELDS = 'People fields'


@api.route(f'/{PEOPLE}/{FIELDS}')
class PeopleFields(Resource):
    """
    Get the People fields.
    """
    def get(self):
        """
        Get the People fields.
        """
        return {PEOPLE_FIELDS: pflds.get_flds()}


PEOPLE_FORM = 'People query form'


@api.route(f'/{PEOPLE}/{FORM}')
class PeopleForm(Resource):
    """
    Get the form for querying the People data.
    """
    def get(self):
        """
        Get the form for querying the People data.
        """
        return {PEOPLE_FORM: pfrm.get_form()}


@api.route(f'/{PEOPLE}/{READ}')
class PeopleRead(Resource):
    """
    This endpoint serves People data as a dict.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Data not found')
    @api.doc(params=pfrm.get_form_descr())
    def get(self):
        """
        Returns People data.
        """
        args = acmn.get_args_from_req(request)
        name = args.get(pflds.NAME)
        role = args.get(rls.ROLE)
        user_id = args.get(pflds.USER_ID)
        people = {}
        if user_id:
            people = pqry.fetch_by_id(user_id)
            return {PEOPLE: people}
        if name:
            name = unquote(args.get(pflds.NAME))
        people = pqry.fetch_all_or_some(name=name, role=role)
        return {PEOPLE: people}


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    pflds.NAME: fields.String,
    pflds.EMAIL: fields.String,
    pflds.AFFILIATION: fields.String,
    EDITOR: fields.String,
})


PEOPLE_CREATE_FORM = 'People Add Form'


@api.route(f'/{PEOPLE}/{CREATE}/{FORM}')
class PeopleAddForm(Resource):
    """
    Form to add a new person to the journal database.
    """
    def get(self):
        return {PEOPLE_CREATE_FORM: pfrm.get_add_form()}


@api.route(f'/{PEOPLE}/{CREATE}')
@api.expect(parser)
class PeopleCreate(Resource):
    """
    Add a person to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        """
        Add a person.
        """
        user_id, auth_key = _get_user_info(request)
        if not sm.is_permitted(PROTOCOL_NM, sm.CREATE, user_id=user_id,
                               auth_key=auth_key):
            raise wz.Forbidden('Action not permitted.')
        try:
            ret = pqry.add(request.json)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            'ret': ret,
        }


@api.route(f'/{PEOPLE}/{DELETE}/<person_id>')
@api.expect(parser)
class PeopleDelete(Resource):
    """
    Deletes an existing person.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Person not found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(api.model('Placeholder', {}))
    def delete(self, person_id):
        user_id, auth_key = _get_user_info(request)
        if not sm.is_permitted(PROTOCOL_NM, sm.DELETE, user_id=user_id,
                               auth_key=auth_key):
            raise wz.Forbidden('Action not permitted.')
        try:
            pqry.delete(person_id)
            return {MESSAGE: 'Person deleted!'}
        except ValueError:
            print(f'Person not found: {person_id}.')
            raise wz.NotFound(f'Person not found: {person_id}')


# @api.route(f'/{PEOPLE}/{RETRIEVE}/<code>')
# class PeopleRetrieve(Resource):
#     """
#     Get a single person.
#     """
#     @api.response(HTTPStatus.OK, 'Success')
#     @api.response(HTTPStatus.NOT_FOUND, 'Data not found')
#     def get(self, code):
#         entry = pqry.fetch_by_key(code)
#         if entry:
#             return entry
#         else:
#             raise wz.NotFound(f'No person entry with {code=}')


@api.route(f'/{PEOPLE}/{UPDATE}/<person_id>')
@api.expect(parser)
class PeopleUpdate(Resource):
    """
    Update a single person.
    The fields we expect ought to be the same as for create.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Person not found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self, person_id):
        user_id, auth_key = _get_user_info(request)
        if not sm.is_permitted(PROTOCOL_NM, sm.UPDATE, user_id=user_id,
                               auth_key=auth_key):
            raise wz.Forbidden('Action not permitted.')
        try:
            if not pqry.update(person_id, request.json):
                raise wz.NotFound(f'{person_id=} not found for updating')
        except ValueError as e:
            raise wz.NotAcceptable(f'Error updating user: {e}')
        return {MESSAGE: 'Person updated.'}


@api.route(f'/{PEOPLE}/{MASTHEAD}')
class PeopleMasthead(Resource):
    """
    Get the journal's masthead.
    """
    def get(self):
        """
        Get the people data for the journal masthead.
        """
        mast = pqry.get_masthead()
        return {MASTHEAD: mast}


def main():
    print('In main')


if __name__ == '__main__':
    main()
