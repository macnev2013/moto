from __future__ import unicode_literals
from moto.core.responses import BaseResponse
from moto.ec2.utils import filters_from_querystring


class TransitGateways(BaseResponse):
    def create_transit_gateway(self):
        description = self._get_param("Description")
        options = self._get_multi_param_helper("Options")
        tags = self._get_multi_param("TagSpecification")
        if tags:
            tags = tags[0].get("Tag")
        transit_gateway = self.ec2_backend.create_transit_gateway(
            description=description, options=options, tags=tags
        )
        template = self.response_template(CREATE_TRANSIT_GATEWAY_RESPONSE)
        return template.render(transit_gateway=transit_gateway)

    def delete_transit_gateway(self):
        transit_gateway_id = self._get_param("TransitGatewayId")
        transit_gateway = self.ec2_backend.delete_nat_gateway(transit_gateway_id)
        template = self.response_template(DELETE_TRANSIT_GATEWAY_RESPONSE)
        return template.render(transit_gateway=transit_gateway)

    def describe_transit_gateways(self):
        filters = filters_from_querystring(self.querystring)
        transit_gateways = self.ec2_backend.get_all_transit_gateways(filters)
        template = self.response_template(DESCRIBE_TRANSIT_GATEWAY_RESPONSE)
        return template.render(transit_gateways=transit_gateways)


CREATE_TRANSIT_GATEWAY_RESPONSE = """<CreateTransitGatewayResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>151283df-f7dc-4317-89b4-01c9888b1d45</requestId>
    <transitGateway>
        <transitGatewayId>{{ transit_gateway.id }}</transitGatewayId>
        <ownerId>{{ transit_gateway.owner_id }}</ownerId>
        <description>{{ transit_gateway.description }}</description>
        <createTime>{{ transit_gateway.create_time }}</createTime>
        <state>{{ transit_gateway.state }}</state>
        {% if transit_gateway.options %}
            <options>
                <amazonSideAsn>{{ transit_gateway.options.AmazonSideAsn }}</amazonSideAsn>
                <associationDefaultRouteTableId>tgw-rtb-002573ed1eEXAMPLE</associationDefaultRouteTableId>
                <autoAcceptSharedAttachments>{{ transit_gateway.options.AutoAcceptSharedAttachments }}</autoAcceptSharedAttachments>
                <defaultRouteTableAssociation>{{ transit_gateway.options.DefaultRouteTableAssociation }}</defaultRouteTableAssociation>
                <defaultRouteTablePropagation>{{ transit_gateway.options.DefaultRouteTablePropagation }}</defaultRouteTablePropagation>
                <dnsSupport>{{ transit_gateway.options.DnsSupport }}</dnsSupport>
                <propagationDefaultRouteTableId>tgw-rtb-002573ed1eEXAMPLE</propagationDefaultRouteTableId>
                <vpnEcmpSupport>{{ transit_gateway.options.VpnEcmpSupport }}</vpnEcmpSupport>
            </options>
        {% endif %}
        {% if transit_gateway.tags %}
            <tagSet>
                {% for tag in transit_gateway.tags %}
                    <item>
                    <key>{{ tag['Key'] }}</key>
                    <value>{{ tag['Value'] }}</value>
                    </item>
                {% endfor %}
            </tagSet>
        {% endif %}
    </transitGateway>
</CreateTransitGatewayResponse>
"""

DESCRIBE_TRANSIT_GATEWAY_RESPONSE = """<DescribeTransitGatewaysResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>151283df-f7dc-4317-89b4-01c9888b1d45</requestId>
    <transitGatewaySet>
    {% for transit_gateway in transit_gateways %}
        <item>
            <creationTime>{{ transit_gateway.create_time }}</creationTime>
            <description>{{ transit_gateway.description }}</description>
            {% if transit_gateway.options %}
                <options>
                    <amazonSideAsn>{{ transit_gateway.options.AmazonSideAsn }}</amazonSideAsn>
                    <associationDefaultRouteTableId>tgw-rtb-002573ed1eEXAMPLE</associationDefaultRouteTableId>
                    <autoAcceptSharedAttachments>{{ transit_gateway.options.AutoAcceptSharedAttachments }}</autoAcceptSharedAttachments>
                    <defaultRouteTableAssociation>{{ transit_gateway.options.DefaultRouteTableAssociation }}</defaultRouteTableAssociation>
                    <defaultRouteTablePropagation>{{ transit_gateway.options.DefaultRouteTablePropagation }}</defaultRouteTablePropagation>
                    <dnsSupport>{{ transit_gateway.options.DnsSupport }}</dnsSupport>
                    <propagationDefaultRouteTableId>tgw-rtb-002573ed1eEXAMPLE</propagationDefaultRouteTableId>
                    <vpnEcmpSupport>{{ transit_gateway.options.VpnEcmpSupport }}</vpnEcmpSupport>
                </options>
            {% endif %}
            <ownerId>{{ transit_gateway.owner_id }}</ownerId>
            <state>{{ transit_gateway.state }}</state>
            {% if transit_gateway.tags %}
            <tagSet>
                {% for tag in transit_gateway.tags %}
                    <item>
                    <key>{{ tag['Key'] }}</key>
                    <value>{{ tag['Value'] }}</value>
                    </item>
                {% endfor %}
            </tagSet>
            {% endif %}
            <transitGatewayArn>arn:aws:ec2:us-east-1:{{ transit_gateway.owner_id }}:transit-gateway/{{ transit_gateway.id }}</transitGatewayArn>
            <transitGatewayId>{{ transit_gateway.id }}</transitGatewayId>
        </item>
    {% endfor %}
    </transitGatewaySet>
</DescribeTransitGatewaysResponse>
"""

DELETE_TRANSIT_GATEWAY_RESPONSE = """<DeleteTransitGatewayResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>151283df-f7dc-4317-89b4-01c9888b1d45</requestId>
    <transitGatewayId>{{ transit_gateway.id }}</transitGatewayId>
</DeleteTransitGatewayResponse>
"""
