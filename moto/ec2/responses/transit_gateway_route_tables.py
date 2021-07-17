from __future__ import unicode_literals
from moto.core.responses import BaseResponse


class TransitGatewayRouteTable(BaseResponse):
    def create_transit_gateway_route_table(self):
        transit_gateway_id = self._get_param("TransitGatewayId")
        tags = self._get_multi_param("TagSpecification")
        tags = tags[0] if isinstance(tags, list) and len(tags) == 1 else tags
        tags = (tags or {}).get("Tag", [])
        tags = {t["Key"]: t["Value"] for t in tags}

        transit_gateway_route_table = self.ec2_backend.create_transit_gateway_route_table(
            transit_gateway_id=transit_gateway_id, tags=tags
        )
        template = self.response_template(CREATE_TRANSIT_GATEWAY_ROUTE_TABLE_RESPONSE)
        return template.render(transit_gateway_route_table=transit_gateway_route_table)


CREATE_TRANSIT_GATEWAY_ROUTE_TABLE_RESPONSE = """<CreateTransitGatewayRouteTableResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>3a495d25-08d4-466d-822e-477c9b1fc606</requestId>
    <transitGatewayRouteTable>
        <creationTime>{{ transit_gateway_route_table._created_at }}</creationTime>
        <defaultAssociationRouteTable>{{ transit_gateway_route_table.default_association_route_table }}</defaultAssociationRouteTable>
        <defaultPropagationRouteTable>{{ transit_gateway_route_table.default_propagation_route_table }}</defaultPropagationRouteTable>
        <state>{{ transit_gateway_route_table.state }}</state>
        <transitGatewayId>{{ transit_gateway_route_table.transit_gateway_id }}</transitGatewayId>
        <transitGatewayRouteTableId>{{ transit_gateway_route_table.id }}</transitGatewayRouteTableId>
    </transitGatewayRouteTable>
</CreateTransitGatewayRouteTableResponse>
"""
