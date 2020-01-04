from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from storeManage import models
from base.models import UserNow, Area
from base.models import Organization, Material, Department
# from .Serializer import
import json
