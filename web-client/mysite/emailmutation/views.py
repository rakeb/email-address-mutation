import datetime
import json
import logging
import time

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from emailmutation.email_receive.verification import process_email_for_verification
from emailmutation.email_sender.mutation import process_email_for_mutation
from emailmutation.models import MutationParam, AllVipEmail, AllShadowEmail

# MutationParam.objects.all()

logger = logging.getLogger('views.py')
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# http://127.0.0.1:8000/emailmutation/setparam/
# {
# 	"email_address": "alice.email.mutation@gmail.com",
# 	"password": "emailmutation",
# 	"last_n_email_hash": ["a", "b", "c"],
# 	"shadow_list": [
# 			{
# 				"email_address": "alice.email.mutation.1@gmail.com",
# 				"password": "emailmutation"
# 			},
# 			{
# 				"email_address": "alice.email.mutation.2@gmail.com",
# 				"password": "emailmutation"
# 			}
# 		]
# }

@csrf_exempt
def set_user_mutation_param(request):
    if request.method == 'POST':
        json_loads = json.loads(request.body.decode("utf-8"))
        email_address = json_loads['email_address']
        # last_n_email_hash = json_loads['last_n_email_hash']
        shadow_list = json_loads['shadow_list']
        password = json_loads['password']
        all_shadow = json_loads['all_shadow']
        all_vip = json_loads['all_vip']
        # mutation_param_obj = MutationParam(email_address=email_address, shadow_list=shadow_list, password=password)
        # mutation_param_obj.save()

        obj, created = MutationParam.objects.update_or_create(email_address=email_address, shadow_list=shadow_list,
                                                              password=password)

        for vip in all_vip:
            obj, created = AllVipEmail.objects.update_or_create(vip_email=vip)

        for shadow in all_shadow:
            obj, created = AllShadowEmail.objects.update_or_create(shadow_email=shadow)

        logger.debug("User: {} mutation param saved to DB".format(email_address))
        output_json = {'status': 'success'}
    else:
        output_json = {'status': 'failed'}
    logger.info("Sending response to client: {}".format(output_json))
    return HttpResponse(
        json.dumps(output_json),
        content_type="application/json"
    )


@csrf_exempt
def send_mail(request):
    if request.method == 'POST':
        json_loads = json.loads(request.body.decode("utf-8"))
        logger.info("Mutation API called: {}".format(json_loads))
        a = datetime.datetime.now()
        process_email_for_mutation(json_loads)
        # time.sleep(5)
        b = datetime.datetime.now()
        c = b - a
        logger.info("End-to-end Email sending time in milliseconds: {}".format(c.microseconds / 1000))

        with open('8000_multi_org_em_overhead.txt', 'a') as f:
            f.write("{} \n".format(c.microseconds / 1000))

        # email_address = json_loads['email_address']
        # last_n_email_hash = json_loads['last_n_email_hash']
        # shadow_list = json_loads['shadow_list']
        # password = json_loads['password']
        # mutation_param_obj = UserMutationParam(email_address=email_address, last_n_email_hash=last_n_email_hash,
        #                                        shadow_list=shadow_list, password=password)
        # mutation_param_obj.save()
        # logger.debug("User: {} mutation param saved to DB".format(email_address))
        output_json = {'status': 'Email successfully sent'}
    else:
        output_json = {'status': 'Failed to send email'}
    logger.info("Sending response to client: {}".format(output_json))
    return HttpResponse(
        # json.dumps(output_json),
        json.dumps(output_json['status']),
        content_type="application/json"
    )


@csrf_exempt
def receive_mail(request):
    if request.method == 'POST':
        json_loads = json.loads(request.body.decode("utf-8"))
        logger.info("Verification API called: {}".format(json_loads))
        a = datetime.datetime.now()
        status = process_email_for_verification(json_loads)
        # time.sleep(10)
        # status = 'false'
        b = datetime.datetime.now()
        c = b - a
        logger.info("End-to-end Email verification time in milliseconds: {}".format(c.microseconds / 1000))
        with open('30_email_verification.txt', 'a') as f:
            f.write("{} \n".format(c.microseconds / 1000))
        if status is None:
            output_json = {'status': 'Verification not required'}
        elif status is True:
            output_json = {'status': 'Verification successful'}
        else:
            output_json = {'status': 'Verification failed'}
    else:
        output_json = {'status': 'Verification failed'}
    logger.info("Sending response to client: {}".format(output_json))
    return HttpResponse(
        json.dumps(output_json['status']),
        content_type="application/json"
    )
